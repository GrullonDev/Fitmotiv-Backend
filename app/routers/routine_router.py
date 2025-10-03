"""
Routine router - handles routine and workout management
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.models import Routine, RoutineExercise, Exercise, User, WorkoutSession
from app import schemas
from app.schemas import (
    RoutineCreate, RoutineResponse, RoutineUpdate, MessageResponse,
    RoutineExerciseCreate, RoutineExerciseResponse, RoutineExerciseUpdate,
    WorkoutSessionCreate, WorkoutSessionResponse
)
from app.security import get_current_user

router = APIRouter(prefix="/api/routines", tags=["Rutinas"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=List[RoutineResponse])
async def get_routines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    difficulty: Optional[str] = Query(None, description="Filtrar por dificultad"),
    is_public: bool = Query(False, description="Mostrar rutinas públicas"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener rutinas del usuario o rutinas públicas
    """
    query = db.query(Routine)
    
    if is_public:
        query = query.filter(Routine.is_public == True)
    else:
        query = query.filter(Routine.user_id == current_user.id)
    
    # Aplicar filtros
    if category:
        query = query.filter(Routine.category == category)
    
    if difficulty:
        query = query.filter(Routine.difficulty_level == difficulty)
    
    routines = query.offset(skip).limit(limit).all()
    return routines


@router.get("/{routine_id}", response_model=RoutineResponse)
async def get_routine(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener una rutina específica por ID
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Verificar permisos: propietario o rutina pública
    if routine.user_id != current_user.id and not routine.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta rutina"
        )
    
    return routine


@router.post("/", response_model=RoutineResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def create_routine(
    request: Request,
    routine: RoutineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva rutina
    """
    # Verificar si ya existe una rutina con el mismo nombre del usuario
    existing_routine = db.query(Routine).filter(
        Routine.name == routine_data.name,
        Routine.user_id == current_user.id
    ).first()
    
    if existing_routine:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya tienes una rutina con ese nombre"
        )
    
    # Crear nueva rutina
    routine = Routine(
        **routine_data.model_dump(),
        user_id=current_user.id
    )
    
    db.add(routine)
    db.commit()
    db.refresh(routine)
    
    return routine


@router.put("/{routine_id}", response_model=RoutineResponse)
async def update_routine(
    routine_id: int,
    routine_data: RoutineUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar una rutina (solo el propietario)
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Solo el propietario puede editar
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta rutina"
        )
    
    # Actualizar campos
    update_data = routine_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(routine, field, value)
    
    db.commit()
    db.refresh(routine)
    
    return routine


@router.delete("/{routine_id}", response_model=MessageResponse)
async def delete_routine(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una rutina (solo el propietario)
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Solo el propietario puede eliminar
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta rutina"
        )
    
    db.delete(routine)
    db.commit()
    
    return MessageResponse(message="Rutina eliminada correctamente")


# Endpoints para ejercicios en rutinas
@router.get("/{routine_id}/exercises", response_model=List[RoutineExerciseResponse])
async def get_routine_exercises(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener ejercicios de una rutina específica
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Verificar permisos
    if routine.user_id != current_user.id and not routine.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta rutina"
        )
    
    exercises = db.query(RoutineExercise).filter(
        RoutineExercise.routine_id == routine_id
    ).order_by(RoutineExercise.order_in_routine).all()
    
    return exercises


@router.post("/{routine_id}/exercises", response_model=RoutineExerciseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def add_exercise_to_routine(
    request: Request,
    routine_id: int,
    routine_exercise: RoutineExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Agregar un ejercicio a una rutina
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Solo el propietario puede modificar
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta rutina"
        )
    
    # Verificar que el ejercicio existe
    exercise = db.query(Exercise).filter(Exercise.id == exercise_data.exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado"
        )
    
    # Determinar el orden si no se especifica
    if exercise_data.order_in_routine is None:
        max_order = db.query(RoutineExercise).filter(
            RoutineExercise.routine_id == routine_id
        ).count()
        exercise_data.order_in_routine = max_order + 1
    
    # Crear la asociación
    routine_exercise = RoutineExercise(
        routine_id=routine_id,
        **exercise_data.model_dump()
    )
    
    db.add(routine_exercise)
    db.commit()
    db.refresh(routine_exercise)
    
    return routine_exercise


@router.put("/{routine_id}/exercises/{exercise_id}", response_model=RoutineExerciseResponse)
async def update_routine_exercise(
    routine_id: int,
    exercise_id: int,
    exercise_data: RoutineExerciseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar un ejercicio en una rutina
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Solo el propietario puede modificar
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta rutina"
        )
    
    routine_exercise = db.query(RoutineExercise).filter(
        RoutineExercise.routine_id == routine_id,
        RoutineExercise.id == exercise_id
    ).first()
    
    if not routine_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado en la rutina"
        )
    
    # Actualizar campos
    update_data = exercise_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(routine_exercise, field, value)
    
    db.commit()
    db.refresh(routine_exercise)
    
    return routine_exercise


@router.delete("/{routine_id}/exercises/{exercise_id}", response_model=MessageResponse)
async def remove_exercise_from_routine(
    routine_id: int,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar un ejercicio de una rutina
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Solo el propietario puede modificar
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta rutina"
        )
    
    routine_exercise = db.query(RoutineExercise).filter(
        RoutineExercise.routine_id == routine_id,
        RoutineExercise.id == exercise_id
    ).first()
    
    if not routine_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado en la rutina"
        )
    
    db.delete(routine_exercise)
    db.commit()
    
    return MessageResponse(message="Ejercicio eliminado de la rutina")


# Endpoints para sesiones de entrenamiento
@router.post("/{routine_id}/workout-sessions", response_model=WorkoutSessionResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def start_workout(
    request: Request,
    routine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Iniciar una sesión de entrenamiento con una rutina
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Verificar permisos
    if routine.user_id != current_user.id and not routine.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para usar esta rutina"
        )
    
    # Crear nueva sesión de entrenamiento
    from datetime import datetime
    workout_session = WorkoutSession(
        user_id=current_user.id,
        routine_id=routine_id,
        start_time=datetime.utcnow()
    )
    
    db.add(workout_session)
    db.commit()
    db.refresh(workout_session)
    
    return workout_session


@router.get("/favorites/", response_model=List[RoutineResponse])
async def get_favorite_routines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener rutinas marcadas como favoritas del usuario
    """
    routines = db.query(Routine).filter(
        Routine.user_id == current_user.id,
        Routine.is_favorite == True
    ).all()
    
    return routines


@router.post("/{routine_id}/toggle-favorite", response_model=MessageResponse)
async def toggle_favorite_routine(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marcar/desmarcar una rutina como favorita
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada"
        )
    
    # Solo el propietario puede marcar como favorita
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta rutina"
        )
    
    routine.is_favorite = not routine.is_favorite
    db.commit()
    
    status_msg = "agregada a" if routine.is_favorite else "eliminada de"
    return MessageResponse(message=f"Rutina {status_msg} favoritos")