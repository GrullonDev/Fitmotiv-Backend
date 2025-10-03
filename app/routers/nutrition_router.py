"""
Nutrition router - handles nutrition tracking and meal management
"""
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app import models
from app.models import NutritionEntry, User
from app import schemas
from app.schemas import (
    NutritionEntryCreate, NutritionEntryResponse, NutritionEntryUpdate,
    MessageResponse, NutritionSummaryResponse
)
from app.security import get_current_user

router = APIRouter(prefix="/api/nutrition", tags=["Nutrición"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=List[NutritionEntryResponse])
async def get_nutrition_entries(
    start_date: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    meal_type: Optional[str] = Query(None, description="Tipo de comida (breakfast, lunch, dinner, snack)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener entradas de nutrición del usuario con filtros opcionales
    """
    query = db.query(models.NutritionEntry).filter(models.NutritionEntry.user_id == current_user.id)
    
    # Aplicar filtros de fecha
    if start_date:
        query = query.filter(models.NutritionEntry.date >= start_date)
    
    if end_date:
        query = query.filter(models.NutritionEntry.date <= end_date)
    
    # Filtrar por tipo de comida
    if meal_type:
        query = query.filter(models.NutritionEntry.meal_type == meal_type)
    
    # Ordenar por fecha y hora de creación (más reciente primero)
    entries = query.order_by(
        models.NutritionEntry.date.desc(),
        models.NutritionEntry.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return entries


@router.get("/today", response_model=List[NutritionEntryResponse])
async def get_today_nutrition(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener entradas de nutrición del día actual
    """
    today = date.today()
    entries = db.query(models.NutritionEntry).filter(
        models.NutritionEntry.user_id == current_user.id,
        models.NutritionEntry.date == today
    ).order_by(models.NutritionEntry.created_at).all()
    
    return entries


@router.get("/summary", response_model=NutritionSummaryResponse)
async def get_nutrition_summary(
    target_date: date = Query(default_factory=date.today, description="Fecha para el resumen (YYYY-MM-DD)"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener resumen nutricional de un día específico (calorías totales, macros, etc.)
    """
    # Obtener todas las entradas del día
    entries = db.query(models.NutritionEntry).filter(
        models.NutritionEntry.user_id == current_user.id,
        models.NutritionEntry.date == target_date
    ).all()
    
    # Calcular totales
    total_calories = sum(entry.calories or 0 for entry in entries)
    total_protein = sum(entry.protein or 0 for entry in entries)
    total_carbs = sum(entry.carbohydrates or 0 for entry in entries)
    total_fat = sum(entry.fat or 0 for entry in entries)
    total_fiber = sum(entry.fiber or 0 for entry in entries)
    total_sugar = sum(entry.sugar or 0 for entry in entries)
    total_sodium = sum(entry.sodium or 0 for entry in entries)
    
    # Agrupar por tipo de comida
    meals_summary = {}
    for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
        meal_entries = [e for e in entries if e.meal_type == meal_type]
        meals_summary[meal_type] = {
            "entries_count": len(meal_entries),
            "calories": sum(entry.calories or 0 for entry in meal_entries),
            "protein": sum(entry.protein or 0 for entry in meal_entries),
            "carbs": sum(entry.carbohydrates or 0 for entry in meal_entries),
            "fat": sum(entry.fat or 0 for entry in meal_entries)
        }
    
    return {
        "date": target_date,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbohydrates": total_carbs,
        "total_fat": total_fat,
        "total_fiber": total_fiber,
        "total_sugar": total_sugar,
        "total_sodium": total_sodium,
        "meals_summary": meals_summary,
        "entries_count": len(entries)
    }


@router.get("/weekly-summary")
async def get_weekly_nutrition_summary(
    start_date: date = Query(default_factory=lambda: date.today() - timedelta(days=6)),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener resumen nutricional semanal (últimos 7 días)
    """
    end_date = start_date + timedelta(days=6)
    
    # Consulta agregada por día
    results = db.query(
        models.NutritionEntry.date,
        func.sum(models.NutritionEntry.calories).label('total_calories'),
        func.sum(models.NutritionEntry.protein).label('total_protein'),
        func.sum(models.NutritionEntry.carbohydrates).label('total_carbs'),
        func.sum(models.NutritionEntry.fat).label('total_fat'),
        func.count(models.NutritionEntry.id).label('entries_count')
    ).filter(
        models.NutritionEntry.user_id == current_user.id,
        models.NutritionEntry.date.between(start_date, end_date)
    ).group_by(models.NutritionEntry.date).all()
    
    # Formatear resultados
    daily_summaries = []
    for result in results:
        daily_summaries.append({
            "date": result.date,
            "calories": result.total_calories or 0,
            "protein": result.total_protein or 0,
            "carbs": result.total_carbs or 0,
            "fat": result.total_fat or 0,
            "entries_count": result.entries_count
        })
    
    # Calcular promedios semanales
    total_days = len(daily_summaries)
    if total_days > 0:
        avg_calories = sum(day["calories"] for day in daily_summaries) / total_days
        avg_protein = sum(day["protein"] for day in daily_summaries) / total_days
        avg_carbs = sum(day["carbs"] for day in daily_summaries) / total_days
        avg_fat = sum(day["fat"] for day in daily_summaries) / total_days
    else:
        avg_calories = avg_protein = avg_carbs = avg_fat = 0
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "daily_summaries": daily_summaries,
        "weekly_averages": {
            "calories": round(avg_calories, 2),
            "protein": round(avg_protein, 2),
            "carbs": round(avg_carbs, 2),
            "fat": round(avg_fat, 2)
        }
    }


@router.get("/{entry_id}", response_model=NutritionEntryResponse)
async def get_nutrition_entry(
    entry_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener una entrada de nutrición específica
    """
    entry = db.query(models.NutritionEntry).filter(
        models.NutritionEntry.id == entry_id,
        models.NutritionEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrada de nutrición no encontrada"
        )
    
    return entry


@router.post("/", response_model=NutritionEntryResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_nutrition_entry(
    request: Request,
    entry: NutritionEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Registrar una nueva entrada de nutrición (comida/bebida)
    """
    # Crear nueva entrada
    entry = models.NutritionEntry(
        **entry_data.model_dump(),
        user_id=current_user.id
    )
    
    db.add(entry)
    db.commit()
    db.refresh(entry)
    
    return entry


@router.put("/{entry_id}", response_model=NutritionEntryResponse)
async def update_nutrition_entry(
    entry_id: int,
    entry_data: NutritionEntryUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar una entrada de nutrición existente
    """
    entry = db.query(models.NutritionEntry).filter(
        models.NutritionEntry.id == entry_id,
        models.NutritionEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrada de nutrición no encontrada"
        )
    
    # Actualizar campos
    update_data = entry_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)
    
    db.commit()
    db.refresh(entry)
    
    return entry


@router.delete("/{entry_id}", response_model=MessageResponse)
async def delete_nutrition_entry(
    entry_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una entrada de nutrición
    """
    entry = db.query(models.NutritionEntry).filter(
        models.NutritionEntry.id == entry_id,
        models.NutritionEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrada de nutrición no encontrada"
        )
    
    db.delete(entry)
    db.commit()
    
    return MessageResponse(message="Entrada de nutrición eliminada correctamente")


@router.get("/search/foods")
async def search_foods(
    query: str = Query(..., min_length=2, description="Término de búsqueda para alimentos"),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Buscar alimentos en base de datos externa (simulado)
    En una implementación real, esto consultaría APIs como USDA Food Data Central,
    Edamam, o Spoonacular
    """
    # Simulación de búsqueda de alimentos comunes
    common_foods = [
        {"name": "Manzana", "calories_per_100g": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
        {"name": "Pollo pechuga", "calories_per_100g": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        {"name": "Arroz blanco", "calories_per_100g": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
        {"name": "Huevo", "calories_per_100g": 155, "protein": 13, "carbs": 1.1, "fat": 11},
        {"name": "Avena", "calories_per_100g": 389, "protein": 17, "carbs": 66, "fat": 7},
        {"name": "Plátano", "calories_per_100g": 89, "protein": 1.1, "carbs": 23, "fat": 0.3},
        {"name": "Brócoli", "calories_per_100g": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
        {"name": "Salmon", "calories_per_100g": 208, "protein": 20, "carbs": 0, "fat": 13},
        {"name": "Yogur griego", "calories_per_100g": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        {"name": "Almendras", "calories_per_100g": 579, "protein": 21, "carbs": 22, "fat": 50}
    ]
    
    # Filtrar por término de búsqueda
    query_lower = query.lower()
    matching_foods = [
        food for food in common_foods 
        if query_lower in food["name"].lower()
    ]
    
    return {
        "query": query,
        "results": matching_foods[:limit],
        "count": len(matching_foods)
    }


@router.get("/meal-types/", response_model=List[str])
async def get_meal_types():
    """
    Obtener tipos de comida disponibles
    """
    return ["breakfast", "lunch", "dinner", "snack"]


@router.post("/bulk", response_model=List[NutritionEntryResponse], status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_bulk_nutrition_entries(
    request: Request,
    entries: List[NutritionEntryCreate],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Crear múltiples entradas de nutrición de una vez (útil para importar comidas completas)
    """
    if len(entries_data) > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden crear más de 20 entradas a la vez"
        )
    
    entries = []
    for entry_data in entries_data:
        entry = models.NutritionEntry(
            **entry_data.model_dump(),
            user_id=current_user.id
        )
        entries.append(entry)
    
    db.add_all(entries)
    db.commit()
    
    # Refrescar todas las entradas
    for entry in entries:
        db.refresh(entry)
    
    return entries