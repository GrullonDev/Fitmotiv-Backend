#!/usr/bin/env python3
"""
Script para poblar datos de ejemplo para tracking de progreso y notificaciones
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime, timedelta
from app.database import SessionLocal
from app import models
from sqlalchemy.exc import IntegrityError

def create_sample_progress_data():
    """Create sample progress entries for testing"""
    db = SessionLocal()
    
    try:
        print("📊 Creando datos de ejemplo para tracking de progreso...")
        
        # Find first user (assuming there's at least one user)
        user = db.query(models.User).first()
        if not user:
            print("❌ No hay usuarios en la base de datos. Primero crea un usuario.")
            return
        
        # Create progress entries over the last 30 days
        base_date = date.today() - timedelta(days=30)
        
        progress_entries = []
        for i in range(0, 31, 3):  # Every 3 days
            entry_date = base_date + timedelta(days=i)
            
            # Simulate gradual weight loss and muscle gain
            weight = 80.0 - (i * 0.2)  # Gradual weight loss
            muscle_mass = 35.0 + (i * 0.1)  # Gradual muscle gain
            body_fat = 20.0 - (i * 0.15)  # Gradual body fat loss
            
            # Simulate strength improvements
            bench_press = 60.0 + (i * 1.5)
            squat = 80.0 + (i * 2.0)
            deadlift = 100.0 + (i * 2.5)
            
            entry = models.ProgressEntry(
                user_id=user.id,
                date=entry_date,
                weight=weight,
                body_fat_percentage=max(12.0, body_fat),
                muscle_mass=muscle_mass,
                chest=95.0 + (i * 0.2),
                waist=85.0 - (i * 0.3),
                hips=95.0 - (i * 0.1),
                bicep_left=32.0 + (i * 0.1),
                bicep_right=32.0 + (i * 0.1),
                thigh_left=55.0 + (i * 0.1),
                thigh_right=55.0 + (i * 0.1),
                max_bench_press=bench_press,
                max_squat=squat,
                max_deadlift=deadlift,
                max_pullups=8 + (i // 6),
                max_pushups=25 + (i // 3),
                resting_heart_rate=65 - (i // 10),
                notes=f"Progreso día {i+1} - ¡Mejorando constantemente!"
            )
            progress_entries.append(entry)
        
        db.add_all(progress_entries)
        print(f"✅ Creadas {len(progress_entries)} entradas de progreso")
        
        # Create sample goals
        goals = [
            models.Goal(
                user_id=user.id,
                title="Perder 5kg",
                description="Reducir peso corporal de forma saludable",
                category="weight_loss",
                target_value=75.0,
                current_value=76.0,
                unit="kg",
                target_date=date.today() + timedelta(days=90),
                status="active",
                priority="high"
            ),
            models.Goal(
                user_id=user.id,
                title="Hacer 15 dominadas seguidas",
                description="Mejorar fuerza en la parte superior del cuerpo",
                category="strength",
                target_value=15,
                current_value=8,
                unit="repeticiones",
                target_date=date.today() + timedelta(days=60),
                status="active",
                priority="medium"
            ),
            models.Goal(
                user_id=user.id,
                title="Correr 5km en menos de 25 minutos",
                description="Mejorar resistencia cardiovascular",
                category="endurance",
                target_value=25,
                current_value=30,
                unit="minutos",
                target_date=date.today() + timedelta(days=120),
                status="active",
                priority="medium"
            ),
            models.Goal(
                user_id=user.id,
                title="Reducir grasa corporal a 15%",
                description="Mejorar composición corporal",
                category="weight_loss",
                target_value=15.0,
                current_value=18.5,
                unit="%",
                target_date=date.today() + timedelta(days=180),
                status="active",
                priority="high"
            )
        ]
        
        db.add_all(goals)
        print(f"✅ Creados {len(goals)} objetivos de ejemplo")
        
        db.commit()
        print("✅ Datos de progreso guardados exitosamente!")
        
    except IntegrityError as e:
        print(f"❌ Error de integridad: {e}")
        db.rollback()
    except Exception as e:
        print(f"❌ Error al crear datos de progreso: {e}")
        db.rollback()
    finally:
        db.close()


def create_sample_notifications():
    """Create sample notifications for testing"""
    db = SessionLocal()
    
    try:
        print("🔔 Creando notificaciones de ejemplo...")
        
        # Find first user
        user = db.query(models.User).first()
        if not user:
            print("❌ No hay usuarios en la base de datos.")
            return
        
        # Create notification settings
        settings = models.NotificationSetting(
            user_id=user.id,
            workout_reminders=True,
            goal_milestones=True,
            progress_updates=True,
            achievements=True,
            social_interactions=True,
            reminder_time_morning="08:00",
            reminder_time_evening="18:00",
            quiet_hours_start="22:00",
            quiet_hours_end="07:00"
        )
        
        db.add(settings)
        
        # Create sample notifications
        notifications = [
            models.Notification(
                user_id=user.id,
                title="¡Bienvenido a FitMotiv!",
                body="Tu viaje fitness comienza ahora. ¡Configura tus objetivos y comienza a entrenar!",
                notification_type="custom",
                category="system",
                is_read=False,
                data={"welcome": True, "first_login": True}
            ),
            models.Notification(
                user_id=user.id,
                title="Recordatorio de Entrenamiento",
                body="¡Es hora de entrenar! No dejes que nada te detenga 💪",
                notification_type="workout_reminder",
                category="exercise",
                is_read=False,
                scheduled_for=datetime.now() + timedelta(hours=1),
                data={"reminder_type": "evening_workout"}
            ),
            models.Notification(
                user_id=user.id,
                title="¡Progreso Detectado!",
                body="Has registrado mejoras en tu fuerza. ¡Sigue así!",
                notification_type="progress_update",
                category="progress",
                is_read=True,
                sent_at=datetime.now() - timedelta(hours=2),
                data={"metric": "strength", "improvement": "bench_press"}
            ),
            models.Notification(
                user_id=user.id,
                title="¡Meta Alcanzada!",
                body="Has completado el 25% de tu objetivo 'Perder 5kg' 🎯",
                notification_type="goal_milestone",
                category="progress",
                is_read=False,
                sent_at=datetime.now() - timedelta(days=1),
                data={"goal_id": 1, "milestone": 25, "goal_title": "Perder 5kg"}
            ),
            models.Notification(
                user_id=user.id,
                title="¡Racha de 7 días!",
                body="Has entrenado 7 días seguidos. ¡Tu disciplina es admirable! 🔥",
                notification_type="achievement",
                category="exercise",
                is_read=False,
                sent_at=datetime.now() - timedelta(days=2),
                data={"achievement_type": "consistency", "days": 7}
            )
        ]
        
        db.add_all(notifications)
        print(f"✅ Creadas {len(notifications)} notificaciones de ejemplo")
        
        # Create sample achievements
        achievements = [
            models.Achievement(
                name="Primera Semana",
                description="Completa tu primera semana de entrenamientos",
                category="consistency",
                icon_url="https://example.com/icons/first_week.png",
                badge_color="#4CAF50",
                points=100,
                criteria={"type": "consistency", "days": 7},
                is_active=True
            ),
            models.Achievement(
                name="Fuerza Creciente",
                description="Aumenta tu peso máximo en press de banca en 10kg",
                category="exercise",
                icon_url="https://example.com/icons/strength.png",
                badge_color="#FF9800",
                points=250,
                criteria={"type": "strength_improvement", "exercise": "bench_press", "improvement": 10},
                is_active=True
            ),
            models.Achievement(
                name="Transformación",
                description="Registra 30 días de progreso corporal",
                category="milestones",
                icon_url="https://example.com/icons/transformation.png",
                badge_color="#9C27B0",
                points=500,
                criteria={"type": "progress_tracking", "days": 30},
                is_active=True
            ),
            models.Achievement(
                name="Objetivo Cumplido",
                description="Completa tu primer objetivo fitness",
                category="milestones",
                icon_url="https://example.com/icons/goal_complete.png",
                badge_color="#2196F3",
                points=300,
                criteria={"type": "goal_completion", "count": 1},
                is_active=True
            )
        ]
        
        db.add_all(achievements)
        print(f"✅ Creados {len(achievements)} logros disponibles")
        
        # Create a user achievement
        user_achievement = models.UserAchievement(
            user_id=user.id,
            achievement_id=1,  # First Week achievement
            progress_value=7.0
        )
        
        db.add(user_achievement)
        print("✅ Asignado logro 'Primera Semana' al usuario")
        
        db.commit()
        print("✅ Notificaciones y logros creados exitosamente!")
        
    except IntegrityError as e:
        print(f"❌ Error de integridad: {e}")
        db.rollback()
    except Exception as e:
        print(f"❌ Error al crear notificaciones: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    print("🚀 Iniciando creación de datos de ejemplo para FitMotiv...")
    print("=" * 50)
    
    create_sample_progress_data()
    print()
    create_sample_notifications()
    
    print("\n" + "=" * 50)
    print("✅ ¡Datos de ejemplo creados exitosamente!")
    print("\n📊 Nuevas funcionalidades disponibles:")
    print("   • Tracking de progreso corporal y fuerza")
    print("   • Sistema de objetivos con seguimiento")
    print("   • Notificaciones push personalizadas")
    print("   • Sistema de logros y gamificación")
    print("   • Análisis de tendencias y reportes")
    print("\n🌐 Visita http://localhost:8000/docs para explorar los nuevos endpoints!")


if __name__ == "__main__":
    main()