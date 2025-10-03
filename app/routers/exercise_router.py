"""
Exercise router - handles exercise CRUD operations
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app import models, schemas
from app.schemas import ExerciseResponse, ExerciseCreate, ExerciseUpdate, MessageResponse
from app.security import get_current_user

router = APIRouter(prefix="/api/exercises", tags=["Ejercicios"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=List[ExerciseResponse])
async def get_exercises(
    skip: int = Query(0, ge=0, description="Número de ejercicios a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de ejercicios a devolver"),
    category: Optional[str] = Query(None, description="Filtrar por categoría (strength, cardio, flexibility, balance)"),
    difficulty: Optional[str] = Query(None, description="Filtrar por dificultad (beginner, intermediate, advanced)"),
    muscle_group: Optional[str] = Query(None, description="Filtrar por grupo muscular"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de ejercicios con filtros opcionales
    """
    query = db.query(models.Exercise)
    
    # Aplicar filtros
    if category:
        query = query.filter(models.Exercise.category == category)
    
    if difficulty:
        query = query.filter(models.Exercise.difficulty_level == difficulty)
    
    if muscle_group:
        # Buscar en el JSON de muscle_groups
        query = query.filter(models.Exercise.muscle_groups.contains([muscle_group]))
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un ejercicio específico por ID
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado"
        )
    return exercise


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_exercise(
    request: Request,
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Crear un nuevo ejercicio personalizado
    """
    # Verificar si ya existe un ejercicio con el mismo nombre del mismo usuario
    existing_exercise = db.query(models.Exercise).filter(
        models.Exercise.name == exercise_data.name,
        models.Exercise.created_by == current_user.id
    ).first()
    
    if existing_exercise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya tienes un ejercicio con ese nombre"
        )
    
    # Crear nuevo ejercicio
    exercise = models.Exercise(
        **exercise_data.model_dump(),
        is_custom=True,
        created_by=current_user.id
    )
    
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar un ejercicio personalizado (solo el creador puede editarlo)
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado"
        )
    
    # Solo el creador puede editar ejercicios personalizados
    if exercise.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este ejercicio"
        )
    
    # Actualizar campos
    update_data = exercise_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exercise, field, value)
    
    db.commit()
    db.refresh(exercise)
    
    return exercise


@router.delete("/{exercise_id}", response_model=MessageResponse)
async def delete_exercise(
    exercise_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar un ejercicio personalizado (solo el creador puede eliminarlo)
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado"
        )
    
    # Solo el creador puede eliminar ejercicios personalizados
    if exercise.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este ejercicio"
        )
    
    # Verificar que no esté siendo usado en rutinas
    from app.models import RoutineExercise
    usage_count = db.query(RoutineExercise).filter(
        Routinemodels.Exercise.exercise_id == exercise_id
    ).count()
    
    if usage_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar el ejercicio porque está siendo usado en {usage_count} rutina(s)"
        )
    
    db.delete(exercise)
    db.commit()
    
    return MessageResponse(message="Ejercicio eliminado correctamente")


@router.get("/categories/", response_model=List[str])
async def get_exercise_categories():
    """
    Obtener lista de categorías de ejercicios disponibles
    """
    return ["strength", "cardio", "flexibility", "balance"]


@router.get("/muscle-groups/", response_model=List[str])
async def get_muscle_groups():
    """
    Obtener lista de grupos musculares disponibles
    """
    return [
        "chest", "back", "shoulders", "biceps", "triceps", "forearms",
        "abs", "obliques", "lower_back", "quadriceps", "hamstrings",
        "glutes", "calves", "tibialis", "full_body"
    ]


@router.get("/my-exercises/", response_model=List[ExerciseResponse])
async def get_my_exercises(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener ejercicios personalizados del usuario actual
    """
    exercises = db.query(models.Exercise).filter(
        models.Exercise.created_by == current_user.id
    ).all()
    
    return exercises