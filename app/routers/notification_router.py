"""
Notification router - handles push notifications, settings, and user preferences
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, or_
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app import models, schemas
from app.schemas import (
    NotificationCreate, NotificationResponse,
    NotificationSettingsCreate, NotificationSettingsUpdate, NotificationSettingsResponse,
    MessageResponse
)
from app.security import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["Notificaciones"])
limiter = Limiter(key_func=get_remote_address)


# Notification Endpoints
@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    is_read: Optional[bool] = Query(None, description="Filtrar por leído/no leído"),
    notification_type: Optional[str] = Query(None, description="Tipo de notificación"),
    category: Optional[str] = Query(None, description="Categoría de notificación"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener notificaciones del usuario"""
    query = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    )
    
    if is_read is not None:
        query = query.filter(models.Notification.is_read == is_read)
    if notification_type:
        query = query.filter(models.Notification.notification_type == notification_type)
    if category:
        query = query.filter(models.Notification.category == category)
    
    notifications = query.order_by(desc(models.Notification.created_at)).offset(skip).limit(limit).all()
    return notifications


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_notification(
    request: Request,
    notification: NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Crear una nueva notificación"""
    db_notification = models.Notification(
        user_id=current_user.id,
        **notification.dict()
    )
    
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # Schedule push notification sending in background
    if notification.scheduled_for is None or notification.scheduled_for <= datetime.now():
        background_tasks.add_task(send_push_notification, db_notification.id, db)
    
    return db_notification


@router.get("/unread-count")
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener número de notificaciones no leídas"""
    count = db.query(models.Notification).filter(
        and_(
            models.Notification.user_id == current_user.id,
            models.Notification.is_read == False
        )
    ).count()
    
    return {"unread_count": count}


@router.put("/{notification_id}/mark-read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Marcar notificación como leída"""
    notification = db.query(models.Notification).filter(
        and_(
            models.Notification.id == notification_id,
            models.Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    
    return notification


@router.put("/mark-all-read", response_model=MessageResponse)
async def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Marcar todas las notificaciones como leídas"""
    db.query(models.Notification).filter(
        and_(
            models.Notification.user_id == current_user.id,
            models.Notification.is_read == False
        )
    ).update({"is_read": True})
    
    db.commit()
    
    return {"message": "Todas las notificaciones marcadas como leídas"}


@router.delete("/{notification_id}", response_model=MessageResponse)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Eliminar una notificación"""
    notification = db.query(models.Notification).filter(
        and_(
            models.Notification.id == notification_id,
            models.Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notificación eliminada exitosamente"}


# Notification Settings Endpoints
@router.get("/settings", response_model=NotificationSettingsResponse)
async def get_notification_settings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener configuración de notificaciones del usuario"""
    settings = db.query(models.NotificationSetting).filter(
        models.NotificationSetting.user_id == current_user.id
    ).first()
    
    if not settings:
        # Create default settings if they don't exist
        settings = models.NotificationSetting(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings


@router.post("/settings", response_model=NotificationSettingsResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_notification_settings(
    request: Request,
    settings: NotificationSettingsCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Crear configuración de notificaciones"""
    # Check if settings already exist
    existing_settings = db.query(models.NotificationSetting).filter(
        models.NotificationSetting.user_id == current_user.id
    ).first()
    
    if existing_settings:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La configuración de notificaciones ya existe para este usuario"
        )
    
    db_settings = models.NotificationSetting(
        user_id=current_user.id,
        **settings.dict()
    )
    
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    
    return db_settings


@router.put("/settings", response_model=NotificationSettingsResponse)
async def update_notification_settings(
    settings: NotificationSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Actualizar configuración de notificaciones"""
    db_settings = db.query(models.NotificationSetting).filter(
        models.NotificationSetting.user_id == current_user.id
    ).first()
    
    if not db_settings:
        # Create settings if they don't exist
        db_settings = models.NotificationSetting(user_id=current_user.id)
        db.add(db_settings)
    
    # Update only provided fields
    update_data = settings.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_settings, field, value)
    
    db.commit()
    db.refresh(db_settings)
    
    return db_settings


@router.post("/settings/device-token", response_model=MessageResponse)
@limiter.limit("20/minute")
async def register_device_token(
    request: Request,
    token: str,
    platform: str = Query(..., regex="^(ios|android)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Registrar token de dispositivo para notificaciones push"""
    settings = db.query(models.NotificationSetting).filter(
        models.NotificationSetting.user_id == current_user.id
    ).first()
    
    if not settings:
        settings = models.NotificationSetting(user_id=current_user.id)
        db.add(settings)
    
    # Update the appropriate token based on platform
    if platform == "ios":
        settings.apns_token = token
    else:  # android
        settings.fcm_token = token
    
    db.commit()
    
    return {"message": f"Token de dispositivo {platform} registrado exitosamente"}


# Scheduled Notifications Endpoints
@router.post("/schedule-workout-reminder", response_model=NotificationResponse)
@limiter.limit("10/minute")
async def schedule_workout_reminder(
    request: Request,
    reminder_time: datetime,
    message: Optional[str] = "¡Es hora de entrenar! 💪",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Programar recordatorio de entrenamiento"""
    # Check user settings to see if workout reminders are enabled
    settings = db.query(models.NotificationSetting).filter(
        models.NotificationSetting.user_id == current_user.id
    ).first()
    
    if settings and not settings.workout_reminders:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los recordatorios de entrenamiento están deshabilitados"
        )
    
    notification = models.Notification(
        user_id=current_user.id,
        title="Recordatorio de Entrenamiento",
        body=message,
        notification_type="workout_reminder",
        category="exercise",
        scheduled_for=reminder_time,
        data={"reminder_type": "workout", "scheduled_by_user": True}
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return notification


@router.get("/scheduled", response_model=List[NotificationResponse])
async def get_scheduled_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener notificaciones programadas del usuario"""
    notifications = db.query(models.Notification).filter(
        and_(
            models.Notification.user_id == current_user.id,
            models.Notification.scheduled_for.isnot(None),
            models.Notification.scheduled_for > datetime.now(),
            models.Notification.is_sent == False
        )
    ).order_by(models.Notification.scheduled_for).offset(skip).limit(limit).all()
    
    return notifications


@router.delete("/scheduled/{notification_id}", response_model=MessageResponse)
async def cancel_scheduled_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Cancelar una notificación programada"""
    notification = db.query(models.Notification).filter(
        and_(
            models.Notification.id == notification_id,
            models.Notification.user_id == current_user.id,
            models.Notification.is_sent == False
        )
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación programada no encontrada"
        )
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notificación programada cancelada"}


# System notification functions
async def send_push_notification(notification_id: int, db: Session):
    """
    Background task to send push notification to user's device
    This is a placeholder - in production, this would integrate with 
    Firebase Cloud Messaging (FCM) or Apple Push Notification Service (APNS)
    """
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id
    ).first()
    
    if not notification:
        return
    
    # Get user's device tokens
    settings = db.query(models.NotificationSetting).filter(
        models.NotificationSetting.user_id == notification.user_id
    ).first()
    
    if not settings:
        return
    
    # In a real implementation, you would:
    # 1. Use FCM SDK or APNS to send the notification
    # 2. Handle different platforms (iOS/Android)
    # 3. Retry logic for failed sends
    # 4. Handle token refreshing
    
    # For now, just mark as sent
    notification.is_sent = True
    notification.sent_at = datetime.now()
    db.commit()
    
    print(f"📱 Push notification sent: {notification.title} - {notification.body}")


async def create_goal_milestone_notification(
    user_id: int, 
    goal_title: str, 
    progress_percentage: float,
    db: Session
):
    """Create notification when user reaches a goal milestone"""
    if progress_percentage in [25, 50, 75, 100]:
        milestone_messages = {
            25: f"¡Excelente! Has completado el 25% de tu objetivo '{goal_title}' 🎯",
            50: f"¡Vas por la mitad! 50% completado de '{goal_title}' 💪",
            75: f"¡Casi ahí! 75% completado de '{goal_title}' 🔥",
            100: f"¡Felicitaciones! Has completado tu objetivo '{goal_title}' 🎉"
        }
        
        notification = models.Notification(
            user_id=user_id,
            title="¡Hito Alcanzado!",
            body=milestone_messages[progress_percentage],
            notification_type="goal_milestone",
            category="progress",
            data={
                "goal_title": goal_title,
                "progress_percentage": progress_percentage,
                "milestone": True
            }
        )
        
        db.add(notification)
        db.commit()


async def create_consistency_notification(user_id: int, days_consistent: int, db: Session):
    """Create notification for workout consistency achievements"""
    consistency_milestones = {
        7: "¡Una semana completa de entrenamientos! 🗓️",
        14: "¡Dos semanas seguidas! Tu disciplina es impresionante 💪",
        30: "¡Un mes completo de entrenamientos! Eres una máquina 🔥",
        90: "¡3 meses consecutivos! Tu dedicación es inspiradora 🏆"
    }
    
    if days_consistent in consistency_milestones:
        notification = models.Notification(
            user_id=user_id,
            title="¡Racha de Entrenamientos!",
            body=consistency_milestones[days_consistent],
            notification_type="achievement",
            category="exercise",
            data={
                "achievement_type": "consistency",
                "days_consistent": days_consistent
            }
        )
        
        db.add(notification)
        db.commit()