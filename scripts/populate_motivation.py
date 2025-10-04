#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de ejemplo para el sistema de motivación diaria
"""
import sys
import os
from datetime import date, datetime, timedelta

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import models

def create_daily_quotes():
    """Crear quotes motivacionales de ejemplo"""
    quotes_data = [
        {
            "quote": "El éxito no es definitivo, el fracaso no es fatal: es el coraje de continuar lo que cuenta.",
            "author": "Winston Churchill",
            "category": "motivation",
            "language": "es",
            "tags": ["perseverancia", "éxito", "coraje"]
        },
        {
            "quote": "Tu cuerpo puede hacerlo. Es tu mente a la que tienes que convencer.",
            "author": "Anónimo",
            "category": "fitness",
            "language": "es",
            "tags": ["mente", "cuerpo", "entrenamiento"]
        },
        {
            "quote": "No se trata de ser perfecto, se trata de ser mejor que ayer.",
            "author": "Anónimo",
            "category": "motivation",
            "language": "es",
            "tags": ["progreso", "mejora", "constancia"]
        },
        {
            "quote": "La fuerza no viene de la capacidad física. Viene de una voluntad indomable.",
            "author": "Mahatma Gandhi",
            "category": "strength",
            "language": "es",
            "tags": ["fuerza", "voluntad", "mental"]
        },
        {
            "quote": "El dolor es temporal, pero rendirse dura para siempre.",
            "author": "Anónimo",
            "category": "fitness",
            "language": "es",
            "tags": ["dolor", "persistencia", "nunca rendirse"]
        },
        {
            "quote": "Lo que no te desafía, no te cambia.",
            "author": "Fred DeVito",
            "category": "fitness",
            "language": "es",
            "tags": ["desafío", "cambio", "crecimiento"]
        },
        {
            "quote": "La salud es riqueza real y no piezas de oro y plata.",
            "author": "Mahatma Gandhi",
            "category": "health",
            "language": "es",
            "tags": ["salud", "bienestar", "vida"]
        },
        {
            "quote": "Un objetivo sin un plan es solo un deseo.",
            "author": "Antoine de Saint-Exupéry",
            "category": "success",
            "language": "es",
            "tags": ["objetivos", "planificación", "éxito"]
        },
        {
            "quote": "La disciplina es el puente entre las metas y los logros.",
            "author": "Jim Rohn",
            "category": "motivation",
            "language": "es",
            "tags": ["disciplina", "metas", "logros"]
        },
        {
            "quote": "Cada entrenamiento te acerca un paso más a tu mejor versión.",
            "author": "Anónimo",
            "category": "fitness",
            "language": "es",
            "tags": ["entrenamiento", "progreso", "superación"]
        },
        {
            "quote": "No busques excusas, busca resultados.",
            "author": "Anónimo",
            "category": "mindset",
            "language": "es",
            "tags": ["excusas", "resultados", "mentalidad"]
        },
        {
            "quote": "La constancia vence lo que la dicha no alcanza.",
            "author": "Proverbio",
            "category": "motivation",
            "language": "es",
            "tags": ["constancia", "persistencia", "éxito"]
        },
        {
            "quote": "Tu única competencia eres tú mismo de ayer.",
            "author": "Anónimo",
            "category": "motivation",
            "language": "es",
            "tags": ["competencia", "superación", "crecimiento"]
        },
        {
            "quote": "Los campeones siguen jugando hasta que lo hacen bien.",
            "author": "Billie Jean King",
            "category": "success",
            "language": "es",
            "tags": ["campeones", "práctica", "excelencia"]
        },
        {
            "quote": "El ejercicio no solo cambia tu cuerpo, cambia tu mente, tu actitud y tu humor.",
            "author": "Anónimo",
            "category": "fitness",
            "language": "es",
            "tags": ["ejercicio", "mente", "actitud", "humor"]
        }
    ]
    
    return quotes_data

def create_daily_challenges():
    """Crear desafíos diarios de ejemplo"""
    challenges_data = [
        {
            "title": "100 Flexiones Challenge",
            "description": "Completa 100 flexiones durante el día, divididas en series.",
            "difficulty_level": "medium",
            "category": "strength",
            "points_reward": 25,
            "estimated_duration": 15,
            "instructions": [
                "Divide las 100 flexiones en series manejables",
                "Mantén buena forma en cada repetición",
                "Descansa entre series según sea necesario",
                "Puedes hacerlas a lo largo del día"
            ],
            "requirements": ["Espacio para hacer flexiones"]
        },
        {
            "title": "Caminata de 10,000 Pasos",
            "description": "Alcanza los 10,000 pasos durante el día.",
            "difficulty_level": "easy",
            "category": "cardio",
            "points_reward": 15,
            "estimated_duration": 60,
            "instructions": [
                "Usa un contador de pasos o app móvil",
                "Camina durante descansos del trabajo",
                "Toma las escaleras en lugar del elevador",
                "Estaciona más lejos de tu destino"
            ],
            "requirements": ["Contador de pasos (smartphone o smartwatch)"]
        },
        {
            "title": "Plancha por 5 Minutos",
            "description": "Mantén la posición de plancha durante un total de 5 minutos.",
            "difficulty_level": "hard",
            "category": "strength",
            "points_reward": 30,
            "estimated_duration": 10,
            "instructions": [
                "Mantén el cuerpo recto desde cabeza a pies",
                "Activa el core durante toda la plancha",
                "Respira normalmente",
                "Puedes dividir en múltiples series"
            ],
            "requirements": ["Colchoneta o superficie cómoda"]
        },
        {
            "title": "Hidratación Consciente",
            "description": "Bebe al menos 8 vasos de agua durante el día.",
            "difficulty_level": "easy",
            "category": "nutrition",
            "points_reward": 10,
            "estimated_duration": 480,
            "instructions": [
                "Bebe un vaso al levantarte",
                "Mantén una botella de agua siempre visible",
                "Programa recordatorios cada 2 horas",
                "Bebe antes de cada comida"
            ],
            "requirements": ["Botella de agua reutilizable"]
        },
        {
            "title": "Meditación de 10 Minutos",
            "description": "Dedica 10 minutos a la meditación o mindfulness.",
            "difficulty_level": "easy",
            "category": "mindfulness",
            "points_reward": 15,
            "estimated_duration": 10,
            "instructions": [
                "Encuentra un lugar tranquilo",
                "Siéntate cómodamente con la espalda recta",
                "Enfócate en tu respiración",
                "Si tu mente divaga, regresa gentilmente al presente"
            ],
            "requirements": ["Lugar tranquilo", "Opcional: app de meditación"]
        },
        {
            "title": "Escaleras en lugar de Elevador",
            "description": "Usa las escaleras en lugar del elevador todo el día.",
            "difficulty_level": "easy",
            "category": "cardio",
            "points_reward": 12,
            "estimated_duration": 5,
            "instructions": [
                "Toma las escaleras en tu edificio",
                "Sube de dos en dos escalones si puedes",
                "Mantén un ritmo constante",
                "Usa la barandilla si es necesario"
            ],
            "requirements": ["Acceso a escaleras"]
        },
        {
            "title": "30 Minutos de Estiramientos",
            "description": "Dedica 30 minutos a estiramientos y flexibilidad.",
            "difficulty_level": "medium",
            "category": "flexibility",
            "points_reward": 20,
            "estimated_duration": 30,
            "instructions": [
                "Calienta ligeramente antes de estirar",
                "Mantén cada estiramiento por 20-30 segundos",
                "No rebotes, mantén estiramientos estáticos",
                "Enfócate en músculos tensos"
            ],
            "requirements": ["Colchoneta", "Ropa cómoda"]
        },
        {
            "title": "Sin Azúcar Agregada",
            "description": "Pasa todo el día sin consumir azúcar agregada.",
            "difficulty_level": "medium",
            "category": "nutrition",
            "points_reward": 25,
            "estimated_duration": 1440,
            "instructions": [
                "Lee las etiquetas de los alimentos",
                "Evita bebidas azucaradas",
                "Elige frutas en lugar de dulces",
                "Usa endulzantes naturales si es necesario"
            ],
            "requirements": ["Planificación de comidas"]
        },
        {
            "title": "Burpees Power Hour",
            "description": "Haz 50 burpees distribuidos en una hora.",
            "difficulty_level": "hard",
            "category": "cardio",
            "points_reward": 35,
            "estimated_duration": 60,
            "instructions": [
                "Divide en series de 5-10 burpees",
                "Descansa entre series",
                "Mantén buena forma en cada repetición",
                "Hidrátate adecuadamente"
            ],
            "requirements": ["Espacio para ejercicio", "Toalla", "Agua"]
        },
        {
            "title": "Gratitud y Reflexión",
            "description": "Escribe 3 cosas por las que estás agradecido y reflexiona sobre tu día.",
            "difficulty_level": "easy",
            "category": "mindfulness",
            "points_reward": 10,
            "estimated_duration": 10,
            "instructions": [
                "Busca un momento tranquilo al final del día",
                "Escribe genuinamente lo que sientes",
                "Reflexiona sobre tus logros del día",
                "Piensa en cómo puedes mejorar mañana"
            ],
            "requirements": ["Cuaderno", "Bolígrafo"]
        }
    ]
    
    return challenges_data

def create_motivation_rewards():
    """Crear recompensas de motivación"""
    rewards_data = [
        {
            "name": "Primer Paso",
            "description": "Completaste tu primer desafío diario",
            "reward_type": "challenge_master",
            "requirement_value": 1,
            "requirement_type": "challenges_completed",
            "badge_icon": "🎯",
            "badge_color": "#4CAF50",
            "points_value": 50
        },
        {
            "name": "Guerrero de 7 Días",
            "description": "Mantuviste una racha de ejercicio por 7 días consecutivos",
            "reward_type": "streak_milestone",
            "requirement_value": 7,
            "requirement_type": "streak_days",
            "badge_icon": "🔥",
            "badge_color": "#FF9800",
            "points_value": 100
        },
        {
            "name": "Centurión",
            "description": "Acumulaste 100 puntos de motivación",
            "reward_type": "points_milestone",
            "requirement_value": 100,
            "requirement_type": "total_points",
            "badge_icon": "💯",
            "badge_color": "#2196F3",
            "points_value": 25
        },
        {
            "name": "Maestro de Desafíos",
            "description": "Completaste 10 desafíos diarios",
            "reward_type": "challenge_master",
            "requirement_value": 10,
            "requirement_type": "challenges_completed",
            "badge_icon": "🏆",
            "badge_color": "#FFD700",
            "points_value": 150
        },
        {
            "name": "Consistencia de Hierro",
            "description": "Mantuviste una racha de ejercicio por 30 días",
            "reward_type": "streak_milestone",
            "requirement_value": 30,
            "requirement_type": "streak_days",
            "badge_icon": "💪",
            "badge_color": "#795548",
            "points_value": 500
        },
        {
            "name": "Gladiador de 500",
            "description": "Acumulaste 500 puntos de motivación",
            "reward_type": "points_milestone",
            "requirement_value": 500,
            "requirement_type": "total_points",
            "badge_icon": "⚔️",
            "badge_color": "#9C27B0",
            "points_value": 100
        },
        {
            "name": "Leyenda de 100 Días",
            "description": "Mantuviste una racha increíble de 100 días",
            "reward_type": "streak_milestone",
            "requirement_value": 100,
            "requirement_type": "streak_days",
            "badge_icon": "👑",
            "badge_color": "#E91E63",
            "points_value": 1000
        },
        {
            "name": "Adicto a los Desafíos",
            "description": "Completaste 50 desafíos diarios",
            "reward_type": "challenge_master",
            "requirement_value": 50,
            "requirement_type": "challenges_completed",
            "badge_icon": "🎖️",
            "badge_color": "#607D8B",
            "points_value": 750
        }
    ]
    
    return rewards_data

def create_motivation_levels():
    """Crear niveles de motivación"""
    levels_data = [
        {
            "level_number": 1,
            "name": "Principiante",
            "description": "¡Bienvenido a tu viaje de fitness!",
            "min_points": 0,
            "max_points": 99,
            "level_icon": "🌱",
            "level_color": "#4CAF50",
            "perks": ["Acceso a desafíos básicos"]
        },
        {
            "level_number": 2,
            "name": "Motivado",
            "description": "¡Estás tomando impulso!",
            "min_points": 100,
            "max_points": 299,
            "level_icon": "🌿",
            "level_color": "#8BC34A",
            "perks": ["Desafíos de dificultad media", "Quotes premium"]
        },
        {
            "level_number": 3,
            "name": "Dedicado",
            "description": "Tu compromiso es admirable",
            "min_points": 300,
            "max_points": 599,
            "level_icon": "🌳",
            "level_color": "#689F38",
            "perks": ["Desafíos avanzados", "Estadísticas detalladas"]
        },
        {
            "level_number": 4,
            "name": "Campeón",
            "description": "¡Eres un verdadero guerrero del fitness!",
            "min_points": 600,
            "max_points": 999,
            "level_icon": "🏆",
            "level_color": "#FFD700",
            "perks": ["Desafíos exclusivos", "Insignias especiales", "Análisis avanzado"]
        },
        {
            "level_number": 5,
            "name": "Leyenda",
            "description": "Has alcanzado el estatus de leyenda",
            "min_points": 1000,
            "max_points": None,
            "level_icon": "👑",
            "level_color": "#E91E63",
            "perks": ["Acceso VIP", "Desafíos épicos", "Coach virtual personal", "Comunidad elite"]
        }
    ]
    
    return levels_data

def populate_motivation_data():
    """Poblar la base de datos con datos de motivación"""
    db = SessionLocal()
    
    try:
        print("💪 Creando sistema de motivación diaria...")
        print("=" * 50)
        
        # Crear quotes diarios
        print("📝 Creando quotes motivacionales...")
        quotes_data = create_daily_quotes()
        quote_count = 0
        
        for quote_info in quotes_data:
            existing_quote = db.query(models.DailyQuote).filter(
                models.DailyQuote.quote == quote_info["quote"]
            ).first()
            
            if not existing_quote:
                quote = models.DailyQuote(**quote_info)
                db.add(quote)
                quote_count += 1
        
        print(f"✅ {quote_count} quotes motivacionales creados")
        
        # Crear desafíos diarios
        print("🎯 Creando desafíos diarios...")
        challenges_data = create_daily_challenges()
        challenge_count = 0
        
        for challenge_info in challenges_data:
            existing_challenge = db.query(models.DailyChallenge).filter(
                models.DailyChallenge.title == challenge_info["title"]
            ).first()
            
            if not existing_challenge:
                challenge = models.DailyChallenge(**challenge_info)
                db.add(challenge)
                challenge_count += 1
        
        print(f"✅ {challenge_count} desafíos diarios creados")
        
        # Crear recompensas de motivación
        print("🏆 Creando recompensas de motivación...")
        rewards_data = create_motivation_rewards()
        reward_count = 0
        
        for reward_info in rewards_data:
            existing_reward = db.query(models.MotivationReward).filter(
                models.MotivationReward.name == reward_info["name"]
            ).first()
            
            if not existing_reward:
                reward = models.MotivationReward(**reward_info)
                db.add(reward)
                reward_count += 1
        
        print(f"✅ {reward_count} recompensas de motivación creadas")
        
        # Crear niveles de motivación
        print("📈 Creando niveles de motivación...")
        levels_data = create_motivation_levels()
        level_count = 0
        
        for level_info in levels_data:
            existing_level = db.query(models.MotivationLevel).filter(
                models.MotivationLevel.level_number == level_info["level_number"]
            ).first()
            
            if not existing_level:
                level = models.MotivationLevel(**level_info)
                db.add(level)
                level_count += 1
        
        print(f"✅ {level_count} niveles de motivación creados")
        
        # Commit todos los cambios
        db.commit()
        print("\n" + "=" * 50)
        print("✅ ¡Sistema de motivación diaria creado exitosamente!")
        
        print(f"""
🎉 Resumen de datos creados:
   📝 {quote_count} Quotes motivacionales
   🎯 {challenge_count} Desafíos diarios
   🏆 {reward_count} Recompensas
   📈 {level_count} Niveles de motivación

💪 Funcionalidades disponibles:
   • Quotes motivacionales diarios personalizados
   • Desafíos diarios con diferentes dificultades
   • Sistema de puntos y recompensas
   • Niveles de motivación progresivos
   • Tracking de streaks y consistencia
   • Dashboard completo de motivación

🌐 Nuevos endpoints disponibles en /api/motivation
""")
        
    except Exception as e:
        print(f"❌ Error al crear datos de motivación: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando población de datos de motivación...")
    populate_motivation_data()
    print("🎯 ¡Proceso completado!")