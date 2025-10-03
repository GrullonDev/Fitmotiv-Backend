"""
Progress router - handles progress tracking, goals, and analytics
"""
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, asc
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app import models, schemas
from app.schemas import (
    ProgressEntryCreate, ProgressEntryResponse, ProgressEntryUpdate,
    ProgressReport, ProgressAnalytics,
    GoalCreate, GoalResponse, GoalUpdate,
    MessageResponse
)
from app.security import get_current_user

router = APIRouter(prefix="/api/progress", tags=["Progreso y Objetivos"])
limiter = Limiter(key_func=get_remote_address)


# Progress Entry Endpoints
@router.get("/entries", response_model=List[ProgressEntryResponse])
async def get_progress_entries(
    start_date: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener entradas de progreso del usuario con filtros opcionales"""
    query = db.query(models.ProgressEntry).filter(
        models.ProgressEntry.user_id == current_user.id
    )
    
    if start_date:
        query = query.filter(models.ProgressEntry.date >= start_date)
    if end_date:
        query = query.filter(models.ProgressEntry.date <= end_date)
    
    entries = query.order_by(desc(models.ProgressEntry.date)).offset(skip).limit(limit).all()
    return entries


@router.post("/entries", response_model=ProgressEntryResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def create_progress_entry(
    request: Request,
    entry: ProgressEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Crear una nueva entrada de progreso"""
    # Check if entry for this date already exists
    existing_entry = db.query(models.ProgressEntry).filter(
        and_(
            models.ProgressEntry.user_id == current_user.id,
            models.ProgressEntry.date == entry.date
        )
    ).first()
    
    if existing_entry:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una entrada de progreso para esta fecha"
        )
    
    db_entry = models.ProgressEntry(
        user_id=current_user.id,
        **entry.dict()
    )
    
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return db_entry


@router.get("/entries/{entry_id}", response_model=ProgressEntryResponse)
async def get_progress_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener una entrada de progreso específica"""
    entry = db.query(models.ProgressEntry).filter(
        and_(
            models.ProgressEntry.id == entry_id,
            models.ProgressEntry.user_id == current_user.id
        )
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrada de progreso no encontrada"
        )
    
    return entry


@router.put("/entries/{entry_id}", response_model=ProgressEntryResponse)
async def update_progress_entry(
    entry_id: int,
    entry_data: ProgressEntryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Actualizar una entrada de progreso"""
    entry = db.query(models.ProgressEntry).filter(
        and_(
            models.ProgressEntry.id == entry_id,
            models.ProgressEntry.user_id == current_user.id
        )
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrada de progreso no encontrada"
        )
    
    # Update only provided fields
    update_data = entry_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)
    
    db.commit()
    db.refresh(entry)
    
    return entry


@router.delete("/entries/{entry_id}", response_model=MessageResponse)
async def delete_progress_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Eliminar una entrada de progreso"""
    entry = db.query(models.ProgressEntry).filter(
        and_(
            models.ProgressEntry.id == entry_id,
            models.ProgressEntry.user_id == current_user.id
        )
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrada de progreso no encontrada"
        )
    
    db.delete(entry)
    db.commit()
    
    return {"message": "Entrada de progreso eliminada exitosamente"}


# Analytics Endpoints
@router.get("/analytics/overview", response_model=ProgressReport)
async def get_progress_overview(
    days: int = Query(30, ge=7, le=365, description="Número de días a incluir en el análisis"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener un resumen analítico del progreso"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # Get entries in the specified period
    entries = db.query(models.ProgressEntry).filter(
        and_(
            models.ProgressEntry.user_id == current_user.id,
            models.ProgressEntry.date >= start_date,
            models.ProgressEntry.date <= end_date
        )
    ).order_by(asc(models.ProgressEntry.date)).all()
    
    if not entries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay datos de progreso en el período especificado"
        )
    
    def calculate_analytics(metric_name: str) -> Optional[ProgressAnalytics]:
        values = [getattr(entry, metric_name) for entry in entries if getattr(entry, metric_name) is not None]
        if len(values) < 2:
            return None
        
        current_value = values[-1]
        previous_value = values[0]
        change = current_value - previous_value
        change_percentage = (change / previous_value * 100) if previous_value != 0 else 0
        
        # Determine trend
        if abs(change_percentage) < 1:
            trend = "stable"
        elif change > 0:
            trend = "increasing"
        else:
            trend = "decreasing"
        
        return ProgressAnalytics(
            metric=metric_name,
            current_value=current_value,
            previous_value=previous_value,
            change=change,
            change_percentage=round(change_percentage, 2),
            trend=trend,
            period_days=days
        )
    
    # Calculate analytics for different metrics
    weight_analytics = calculate_analytics("weight")
    body_fat_analytics = calculate_analytics("body_fat_percentage")
    muscle_mass_analytics = calculate_analytics("muscle_mass")
    
    # Strength analytics
    strength_metrics = ["max_bench_press", "max_squat", "max_deadlift", "max_pullups", "max_pushups"]
    strength_analytics = {}
    for metric in strength_metrics:
        analytics = calculate_analytics(metric)
        if analytics:
            strength_analytics[metric] = analytics
    
    # Body measurements analytics
    measurement_metrics = ["chest", "waist", "hips", "bicep_left", "bicep_right", "thigh_left", "thigh_right"]
    measurements_analytics = {}
    for metric in measurement_metrics:
        analytics = calculate_analytics(metric)
        if analytics:
            measurements_analytics[metric] = analytics
    
    # Calculate consistency score
    expected_entries = days // 7  # Expect weekly entries
    actual_entries = len(entries)
    consistency_score = min(100, (actual_entries / expected_entries) * 100) if expected_entries > 0 else 0
    
    return ProgressReport(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        weight_analytics=weight_analytics,
        body_fat_analytics=body_fat_analytics,
        muscle_mass_analytics=muscle_mass_analytics,
        strength_analytics=strength_analytics,
        measurements_analytics=measurements_analytics,
        total_entries=len(entries),
        consistency_score=round(consistency_score, 2)
    )


@router.get("/analytics/trends/{metric}")
async def get_metric_trend(
    metric: str,
    days: int = Query(90, ge=7, le=365),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener tendencia de una métrica específica"""
    valid_metrics = [
        "weight", "body_fat_percentage", "muscle_mass", "chest", "waist", "hips",
        "bicep_left", "bicep_right", "thigh_left", "thigh_right",
        "max_bench_press", "max_squat", "max_deadlift", "max_pullups", "max_pushups",
        "resting_heart_rate", "mile_time_seconds", "flexibility_score"
    ]
    
    if metric not in valid_metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Métrica no válida. Métricas disponibles: {', '.join(valid_metrics)}"
        )
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    entries = db.query(models.ProgressEntry).filter(
        and_(
            models.ProgressEntry.user_id == current_user.id,
            models.ProgressEntry.date >= start_date,
            models.ProgressEntry.date <= end_date,
            getattr(models.ProgressEntry, metric).isnot(None)
        )
    ).order_by(asc(models.ProgressEntry.date)).all()
    
    trend_data = [
        {
            "date": entry.date.isoformat(),
            "value": getattr(entry, metric),
            "notes": entry.notes
        }
        for entry in entries
    ]
    
    return {
        "metric": metric,
        "period_days": days,
        "data_points": len(trend_data),
        "trend_data": trend_data
    }


# Goals Endpoints
@router.get("/goals", response_model=List[GoalResponse])
async def get_goals(
    status: Optional[str] = Query(None, pattern="^(active|completed|paused|cancelled)$"),
    category: Optional[str] = Query(None, pattern="^(weight_loss|muscle_gain|strength|endurance|nutrition|other)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener objetivos del usuario"""
    query = db.query(models.Goal).filter(models.Goal.user_id == current_user.id)
    
    if status:
        query = query.filter(models.Goal.status == status)
    if category:
        query = query.filter(models.Goal.category == category)
    
    goals = query.order_by(desc(models.Goal.created_at)).offset(skip).limit(limit).all()
    
    # Calculate progress percentage and days remaining for each goal
    for goal in goals:
        if goal.target_value and goal.target_value > 0:
            goal.progress_percentage = min(100, (goal.current_value / goal.target_value) * 100)
        else:
            goal.progress_percentage = 0
        
        if goal.target_date:
            days_remaining = (goal.target_date - date.today()).days
            goal.days_remaining = max(0, days_remaining)
        else:
            goal.days_remaining = None
    
    return goals


@router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_goal(
    request: Request,
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Crear un nuevo objetivo"""
    db_goal = models.Goal(
        user_id=current_user.id,
        **goal.dict()
    )
    
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    
    return db_goal


@router.get("/goals/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener un objetivo específico"""
    goal = db.query(models.Goal).filter(
        and_(
            models.Goal.id == goal_id,
            models.Goal.user_id == current_user.id
        )
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    return goal


@router.put("/goals/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Actualizar un objetivo"""
    goal = db.query(models.Goal).filter(
        and_(
            models.Goal.id == goal_id,
            models.Goal.user_id == current_user.id
        )
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    # Update only provided fields
    update_data = goal_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    db.commit()
    db.refresh(goal)
    
    return goal


@router.delete("/goals/{goal_id}", response_model=MessageResponse)
async def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Eliminar un objetivo"""
    goal = db.query(models.Goal).filter(
        and_(
            models.Goal.id == goal_id,
            models.Goal.user_id == current_user.id
        )
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    db.delete(goal)
    db.commit()
    
    return {"message": "Objetivo eliminado exitosamente"}


@router.post("/goals/{goal_id}/update-progress", response_model=GoalResponse)
@limiter.limit("30/minute")
async def update_goal_progress(
    request: Request,
    goal_id: int,
    current_value: float,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Actualizar el progreso de un objetivo"""
    goal = db.query(models.Goal).filter(
        and_(
            models.Goal.id == goal_id,
            models.Goal.user_id == current_user.id
        )
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    goal.current_value = current_value
    
    # Auto-complete goal if target is reached
    if goal.target_value and current_value >= goal.target_value and goal.status == "active":
        goal.status = "completed"
        
        # TODO: Create achievement notification
        # This could trigger a notification about goal completion
    
    db.commit()
    db.refresh(goal)
    
    return goal