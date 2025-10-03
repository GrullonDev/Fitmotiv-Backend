"""
Script para poblar la base de datos con ejercicios de ejemplo
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db, engine, Base
from app.models import Exercise
from datetime import datetime

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# Ejercicios de ejemplo
sample_exercises = [
    # Ejercicios de Fuerza - Pecho
    {
        "name": "Press de Banca",
        "description": "Ejercicio básico para desarrollar el pecho, hombros y tríceps. Acuéstate en un banco y empuja la barra hacia arriba.",
        "category": "strength",
        "muscle_groups": ["chest", "shoulders", "triceps"],
        "equipment_needed": ["barbell", "bench"],
        "difficulty_level": "intermediate",
        "instructions": "1. Acuéstate en el banco con los pies firmes en el suelo\n2. Agarra la barra con las manos ligeramente más separadas que el ancho de los hombros\n3. Baja la barra lentamente hasta tocar el pecho\n4. Empuja la barra hacia arriba hasta extender completamente los brazos",
        "is_custom": False
    },
    {
        "name": "Flexiones de Pecho",
        "description": "Ejercicio de peso corporal que trabaja pecho, hombros y tríceps.",
        "category": "strength",
        "muscle_groups": ["chest", "shoulders", "triceps"],
        "equipment_needed": [],
        "difficulty_level": "beginner",
        "instructions": "1. Posición de plancha con las manos separadas al ancho de los hombros\n2. Mantén el cuerpo recto\n3. Baja el pecho hasta casi tocar el suelo\n4. Empuja hacia arriba hasta la posición inicial",
        "is_custom": False
    },
    
    # Ejercicios de Fuerza - Espalda
    {
        "name": "Dominadas",
        "description": "Ejercicio de peso corporal para fortalecer la espalda y bíceps.",
        "category": "strength",
        "muscle_groups": ["back", "biceps"],
        "equipment_needed": ["pull_up_bar"],
        "difficulty_level": "intermediate",
        "instructions": "1. Cuelga de la barra con agarre pronado\n2. Mantén el cuerpo recto\n3. Tira hacia arriba hasta que el mentón pase la barra\n4. Baja de forma controlada",
        "is_custom": False
    },
    {
        "name": "Remo con Barra",
        "description": "Ejercicio para desarrollar la espalda media y bíceps.",
        "category": "strength",
        "muscle_groups": ["back", "biceps"],
        "equipment_needed": ["barbell"],
        "difficulty_level": "intermediate",
        "instructions": "1. Inclínate hacia adelante con la barra en las manos\n2. Mantén la espalda recta\n3. Tira de la barra hacia el abdomen\n4. Baja de forma controlada",
        "is_custom": False
    },
    
    # Ejercicios de Fuerza - Piernas
    {
        "name": "Sentadillas",
        "description": "Ejercicio fundamental para cuádriceps, glúteos y core.",
        "category": "strength",
        "muscle_groups": ["quadriceps", "glutes", "abs"],
        "equipment_needed": [],
        "difficulty_level": "beginner",
        "instructions": "1. Párate con los pies separados al ancho de los hombros\n2. Baja como si te fueras a sentar en una silla\n3. Mantén las rodillas alineadas con los pies\n4. Sube empujando con los talones",
        "is_custom": False
    },
    {
        "name": "Peso Muerto",
        "description": "Ejercicio compuesto que trabaja toda la cadena posterior.",
        "category": "strength",
        "muscle_groups": ["hamstrings", "glutes", "lower_back"],
        "equipment_needed": ["barbell"],
        "difficulty_level": "advanced",
        "instructions": "1. Párate con la barra sobre los pies\n2. Agáchate y agarra la barra\n3. Mantén la espalda recta y levanta la barra\n4. Extiende las caderas y rodillas al mismo tiempo",
        "is_custom": False
    },
    
    # Ejercicios de Cardio
    {
        "name": "Correr",
        "description": "Actividad cardiovascular básica para mejorar la resistencia.",
        "category": "cardio",
        "muscle_groups": ["quadriceps", "hamstrings", "calves"],
        "equipment_needed": [],
        "difficulty_level": "beginner",
        "instructions": "1. Mantén una postura erguida\n2. Aterriza con el mediopié\n3. Mantén un ritmo constante\n4. Respira de forma rítmica",
        "is_custom": False
    },
    {
        "name": "Burpees",
        "description": "Ejercicio de cuerpo completo que combina fuerza y cardio.",
        "category": "cardio",
        "muscle_groups": ["full_body"],
        "equipment_needed": [],
        "difficulty_level": "intermediate",
        "instructions": "1. Desde de pie, baja a posición de cuclillas\n2. Salta hacia atrás a posición de plancha\n3. Haz una flexión\n4. Salta hacia adelante y luego hacia arriba",
        "is_custom": False
    },
    
    # Ejercicios de Flexibilidad
    {
        "name": "Estiramiento de Isquiotibiales",
        "description": "Estiramiento para mejorar la flexibilidad de la parte posterior de las piernas.",
        "category": "flexibility",
        "muscle_groups": ["hamstrings"],
        "equipment_needed": [],
        "difficulty_level": "beginner",
        "instructions": "1. Siéntate con una pierna extendida\n2. Inclínate hacia adelante desde las caderas\n3. Mantén la posición por 30 segundos\n4. Repite con la otra pierna",
        "is_custom": False
    },
    
    # Ejercicios de Equilibrio
    {
        "name": "Plancha",
        "description": "Ejercicio isométrico para fortalecer el core y mejorar la estabilidad.",
        "category": "balance",
        "muscle_groups": ["abs", "lower_back"],
        "equipment_needed": [],
        "difficulty_level": "beginner",
        "instructions": "1. Apóyate en antebrazos y pies\n2. Mantén el cuerpo recto como una tabla\n3. Contrae el abdomen\n4. Mantén la posición el tiempo indicado",
        "is_custom": False
    },
    
    # Ejercicios adicionales
    {
        "name": "Curl de Bíceps",
        "description": "Ejercicio aislado para desarrollar los bíceps.",
        "category": "strength",
        "muscle_groups": ["biceps"],
        "equipment_needed": ["dumbbells"],
        "difficulty_level": "beginner",
        "instructions": "1. Párate con una mancuerna en cada mano\n2. Mantén los codos pegados al cuerpo\n3. Flexiona los brazos llevando las mancuernas hacia los hombros\n4. Baja de forma controlada",
        "is_custom": False
    },
    {
        "name": "Extensiones de Tríceps",
        "description": "Ejercicio para fortalecer la parte posterior de los brazos.",
        "category": "strength",
        "muscle_groups": ["triceps"],
        "equipment_needed": ["dumbbells"],
        "difficulty_level": "beginner",
        "instructions": "1. Sostén una mancuerna por encima de la cabeza\n2. Baja la mancuerna por detrás de la cabeza\n3. Mantén los codos estables\n4. Extiende los brazos para volver a la posición inicial",
        "is_custom": False
    },
    {
        "name": "Zancadas",
        "description": "Ejercicio unilateral para piernas y glúteos.",
        "category": "strength",
        "muscle_groups": ["quadriceps", "glutes", "hamstrings"],
        "equipment_needed": [],
        "difficulty_level": "beginner",
        "instructions": "1. Da un gran paso hacia adelante\n2. Baja hasta que ambas rodillas formen ángulos de 90 grados\n3. Empuja con el talón delantero para volver\n4. Alterna las piernas",
        "is_custom": False
    }
]

def populate_exercises():
    """Poblar la base de datos con ejercicios de ejemplo"""
    db = next(get_db())
    
    # Verificar si ya existen ejercicios
    existing_count = db.query(Exercise).count()
    if existing_count > 0:
        print(f"La base de datos ya contiene {existing_count} ejercicios.")
        response = input("¿Deseas agregar los ejercicios de ejemplo de todas formas? (y/n): ")
        if response.lower() != 'y':
            print("Operación cancelada.")
            return
    
    # Crear ejercicios
    created_count = 0
    for exercise_data in sample_exercises:
        # Verificar si el ejercicio ya existe
        existing = db.query(Exercise).filter(Exercise.name == exercise_data["name"]).first()
        if existing:
            print(f"El ejercicio '{exercise_data['name']}' ya existe, saltando...")
            continue
        
        exercise = Exercise(**exercise_data)
        db.add(exercise)
        created_count += 1
        print(f"Creado: {exercise_data['name']}")
    
    try:
        db.commit()
        print(f"\n✅ Se crearon {created_count} ejercicios de ejemplo exitosamente!")
        
        # Mostrar resumen por categoría
        print("\n📊 Resumen por categoría:")
        categories = db.query(Exercise.category, db.func.count(Exercise.id)).group_by(Exercise.category).all()
        for category, count in categories:
            print(f"  - {category}: {count} ejercicios")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear ejercicios: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🏋️‍♂️ Poblando la base de datos con ejercicios de ejemplo...")
    populate_exercises()