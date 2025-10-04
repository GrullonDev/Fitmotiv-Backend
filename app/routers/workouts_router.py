"""
Workouts router for daily workout recommendations and tracking
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import date, datetime, timedelta
import random

from app.database import get_db
from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/api/workouts", tags=["Workouts"])


@router.get("/today", response_model=schemas.WorkoutOfTheDayResponse)
async def get_today_workout(
    db: Session = Depends(get_db)
):
    """Get today's workout of the day"""
    today = date.today()
    
    workout = db.query(models.WorkoutOfTheDay).filter(
        models.WorkoutOfTheDay.date == today,
        models.WorkoutOfTheDay.is_active == True
    ).first()
    
    if not workout:
        # If no specific workout for today, get a random active workout
        available_workouts = db.query(models.WorkoutOfTheDay).filter(
            models.WorkoutOfTheDay.is_active == True
        ).all()
        
        if available_workouts:
            workout = random.choice(available_workouts)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No workout available for today"
            )
    
    return workout


@router.get("/", response_model=List[schemas.WorkoutOfTheDayResponse])
async def get_workouts(
    limit: Optional[int] = Query(10, ge=1, le=50),
    category: Optional[str] = Query(None, pattern="^(strength|cardio|flexibility|full_body|hiit)$"),
    difficulty: Optional[str] = Query(None, pattern="^(beginner|intermediate|advanced)$"),
    duration_min: Optional[int] = Query(None, ge=5),
    duration_max: Optional[int] = Query(None, le=180),
    equipment: Optional[str] = None,
    featured_only: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    """Get available workouts with filtering"""
    query = db.query(models.WorkoutOfTheDay).filter(
        models.WorkoutOfTheDay.is_active == True
    )
    
    # Apply filters
    if category:
        query = query.filter(models.WorkoutOfTheDay.category == category)
    if difficulty:
        query = query.filter(models.WorkoutOfTheDay.difficulty_level == difficulty)
    if duration_min:
        query = query.filter(models.WorkoutOfTheDay.estimated_duration >= duration_min)
    if duration_max:
        query = query.filter(models.WorkoutOfTheDay.estimated_duration <= duration_max)
    if equipment:
        query = query.filter(models.WorkoutOfTheDay.equipment_needed.contains([equipment]))
    if featured_only:
        query = query.filter(models.WorkoutOfTheDay.featured == True)
    
    workouts = query.order_by(desc(models.WorkoutOfTheDay.date)).limit(limit).all()
    
    return workouts


@router.get("/{workout_id}", response_model=schemas.WorkoutOfTheDayResponse)
async def get_workout(
    workout_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific workout by ID"""
    workout = db.query(models.WorkoutOfTheDay).filter(
        models.WorkoutOfTheDay.id == workout_id,
        models.WorkoutOfTheDay.is_active == True
    ).first()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    return workout


@router.post("/{workout_id}/complete", response_model=schemas.UserWorkoutCompletionResponse)
async def complete_workout(
    workout_id: int,
    completion: schemas.UserWorkoutCompletionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete a workout and log the session"""
    # Check if workout exists
    workout = db.query(models.WorkoutOfTheDay).filter(
        models.WorkoutOfTheDay.id == workout_id,
        models.WorkoutOfTheDay.is_active == True
    ).first()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    # Check if user already completed this workout today
    today = date.today()
    existing_completion = db.query(models.UserWorkoutCompletion).filter(
        models.UserWorkoutCompletion.user_id == current_user.id,
        models.UserWorkoutCompletion.workout_id == workout_id,
        func.date(models.UserWorkoutCompletion.completed_at) == today
    ).first()
    
    if existing_completion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already completed this workout today"
        )
    
    # Create completion record
    completion_data = completion.dict()
    completion_data["user_id"] = current_user.id
    completion_data["workout_id"] = workout_id
    
    db_completion = models.UserWorkoutCompletion(**completion_data)
    db.add(db_completion)
    
    # Update workout statistics
    workout.completion_count += 1
    
    # Update average rating if provided
    if completion.difficulty_rating or completion.enjoyment_rating:
        # Get all ratings for this workout
        all_completions = db.query(models.UserWorkoutCompletion).filter(
            models.UserWorkoutCompletion.workout_id == workout_id
        ).all()
        
        # Calculate new average rating (using enjoyment rating as primary)
        ratings = []
        for comp in all_completions:
            if comp.enjoyment_rating:
                ratings.append(comp.enjoyment_rating)
        
        if completion.enjoyment_rating:
            ratings.append(completion.enjoyment_rating)
        
        if ratings:
            workout.average_rating = sum(ratings) / len(ratings)
    
    db.commit()
    db.refresh(db_completion)
    
    # Create a workout session record for compatibility
    session_data = {
        "user_id": current_user.id,
        "start_time": datetime.now() - timedelta(minutes=completion.actual_duration or workout.estimated_duration),
        "end_time": datetime.now(),
        "duration_minutes": completion.actual_duration or workout.estimated_duration,
        "calories_burned": completion.calories_burned,
        "notes": completion.notes,
        "rating": completion.enjoyment_rating
    }
    
    workout_session = models.WorkoutSession(**session_data)
    db.add(workout_session)
    db.commit()
    
    return db_completion


@router.get("/my/completions", response_model=List[schemas.UserWorkoutCompletionResponse])
async def get_my_workout_completions(
    limit: Optional[int] = Query(20, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's workout completions"""
    query = db.query(models.UserWorkoutCompletion).filter(
        models.UserWorkoutCompletion.user_id == current_user.id
    )
    
    if start_date:
        query = query.filter(func.date(models.UserWorkoutCompletion.completed_at) >= start_date)
    if end_date:
        query = query.filter(func.date(models.UserWorkoutCompletion.completed_at) <= end_date)
    
    completions = query.order_by(desc(models.UserWorkoutCompletion.completed_at)).limit(limit).all()
    
    return completions


@router.get("/my/stats")
async def get_my_workout_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's workout statistics"""
    # Get all completions
    completions = db.query(models.UserWorkoutCompletion).filter(
        models.UserWorkoutCompletion.user_id == current_user.id
    ).all()
    
    if not completions:
        return {
            "total_workouts": 0,
            "total_time_minutes": 0,
            "total_calories": 0,
            "favorite_category": None,
            "average_rating": 0,
            "current_streak": 0,
            "longest_streak": 0
        }
    
    # Calculate basic stats
    total_workouts = len(completions)
    total_time = sum(c.actual_duration or 0 for c in completions)
    total_calories = sum(c.calories_burned or 0 for c in completions)
    
    # Average ratings
    ratings = [c.enjoyment_rating for c in completions if c.enjoyment_rating]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    # Favorite category (most completed)
    from collections import Counter
    workout_ids = [c.workout_id for c in completions]
    categories = []
    
    for workout_id in workout_ids:
        workout = db.query(models.WorkoutOfTheDay).filter(
            models.WorkoutOfTheDay.id == workout_id
        ).first()
        if workout:
            categories.append(workout.category)
    
    favorite_category = Counter(categories).most_common(1)[0][0] if categories else None
    
    # Calculate streaks
    completion_dates = sorted([
        c.completed_at.date() for c in completions
    ], reverse=True)
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    if completion_dates:
        # Current streak
        today = date.today()
        current_date = today
        
        for completion_date in completion_dates:
            if completion_date == current_date or completion_date == current_date - timedelta(days=1):
                current_streak += 1
                current_date = completion_date - timedelta(days=1)
            else:
                break
        
        # Longest streak
        prev_date = None
        for completion_date in reversed(completion_dates):
            if prev_date is None or completion_date == prev_date + timedelta(days=1):
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
            prev_date = completion_date
    
    # This week's stats
    week_start = date.today() - timedelta(days=date.today().weekday())
    this_week_completions = [
        c for c in completions 
        if c.completed_at.date() >= week_start
    ]
    
    # This month's stats
    month_start = date.today().replace(day=1)
    this_month_completions = [
        c for c in completions 
        if c.completed_at.date() >= month_start
    ]
    
    return {
        "total_workouts": total_workouts,
        "total_time_minutes": total_time,
        "total_calories": total_calories,
        "favorite_category": favorite_category,
        "average_rating": round(avg_rating, 2),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "this_week": {
            "workouts": len(this_week_completions),
            "time_minutes": sum(c.actual_duration or 0 for c in this_week_completions),
            "calories": sum(c.calories_burned or 0 for c in this_week_completions)
        },
        "this_month": {
            "workouts": len(this_month_completions),
            "time_minutes": sum(c.actual_duration or 0 for c in this_month_completions),
            "calories": sum(c.calories_burned or 0 for c in this_month_completions)
        }
    }


@router.get("/recommendations/personalized")
async def get_personalized_workout_recommendations(
    limit: Optional[int] = Query(5, ge=1, le=10),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized workout recommendations based on user profile and history"""
    # Get user profile
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    # Get user's workout history
    completions = db.query(models.UserWorkoutCompletion).filter(
        models.UserWorkoutCompletion.user_id == current_user.id
    ).all()
    
    query = db.query(models.WorkoutOfTheDay).filter(
        models.WorkoutOfTheDay.is_active == True
    )
    
    # Filter by fitness level if available
    if profile and profile.fitness_level:
        if profile.fitness_level == "beginner":
            query = query.filter(models.WorkoutOfTheDay.difficulty_level.in_(["beginner", "intermediate"]))
        elif profile.fitness_level == "intermediate":
            query = query.filter(models.WorkoutOfTheDay.difficulty_level.in_(["intermediate", "advanced"]))
        else:  # advanced
            query = query.filter(models.WorkoutOfTheDay.difficulty_level == "advanced")
    
    # Filter by workout duration preference
    if profile and profile.workout_duration_preference:
        duration_tolerance = 15  # minutes
        query = query.filter(
            models.WorkoutOfTheDay.estimated_duration.between(
                profile.workout_duration_preference - duration_tolerance,
                profile.workout_duration_preference + duration_tolerance
            )
        )
    
    # Filter by available equipment
    if profile and profile.available_equipment:
        # Only show workouts that require equipment the user has
        equipment_filters = []
        for equipment in profile.available_equipment:
            equipment_filters.append(models.WorkoutOfTheDay.equipment_needed.contains([equipment]))
        
        # Also include workouts that require no equipment
        equipment_filters.append(models.WorkoutOfTheDay.equipment_needed.is_(None))
        equipment_filters.append(models.WorkoutOfTheDay.equipment_needed.contains(["none"]))
        
        query = query.filter(func.or_(*equipment_filters))
    
    # Get completed workout IDs to avoid repeating recent workouts
    recent_completion_ids = [c.workout_id for c in completions[-10:]] if completions else []
    if recent_completion_ids:
        query = query.filter(~models.WorkoutOfTheDay.id.in_(recent_completion_ids))
    
    # Get workouts
    recommended_workouts = query.limit(limit * 2).all()  # Get more to allow for randomization
    
    # Randomize and limit
    random.shuffle(recommended_workouts)
    recommended_workouts = recommended_workouts[:limit]
    
    # Add recommendation reason for each workout
    recommendations = []
    for workout in recommended_workouts:
        reason = []
        
        if profile and profile.fitness_level:
            if workout.difficulty_level == profile.fitness_level:
                reason.append(f"Matches your {profile.fitness_level} level")
        
        if profile and profile.workout_duration_preference:
            if abs(workout.estimated_duration - profile.workout_duration_preference) <= 10:
                reason.append(f"Fits your preferred {profile.workout_duration_preference} min duration")
        
        if workout.category == profile.primary_goal if profile and profile.primary_goal else False:
            reason.append(f"Aligns with your {profile.primary_goal} goal")
        
        if not reason:
            reason.append("Highly rated by other users")
        
        recommendations.append({
            "workout": workout,
            "recommendation_reason": ", ".join(reason)
        })
    
    return {"recommendations": recommendations}


@router.get("/categories/stats")
async def get_workout_categories_stats(
    db: Session = Depends(get_db)
):
    """Get statistics for workout categories"""
    stats = db.query(
        models.WorkoutOfTheDay.category,
        func.count(models.WorkoutOfTheDay.id).label("total_workouts"),
        func.avg(models.WorkoutOfTheDay.average_rating).label("avg_rating"),
        func.avg(models.WorkoutOfTheDay.estimated_duration).label("avg_duration"),
        func.sum(models.WorkoutOfTheDay.completion_count).label("total_completions")
    ).filter(
        models.WorkoutOfTheDay.is_active == True
    ).group_by(models.WorkoutOfTheDay.category).all()
    
    return [
        {
            "category": stat.category,
            "total_workouts": stat.total_workouts,
            "average_rating": round(stat.avg_rating or 0, 2),
            "average_duration": round(stat.avg_duration or 0, 1),
            "total_completions": stat.total_completions or 0
        }
        for stat in stats
    ]


@router.post("/{workout_id}/rate")
async def rate_workout(
    workout_id: int,
    rating: int = Query(..., ge=1, le=5),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rate a workout (requires completion)"""
    # Check if user completed this workout
    completion = db.query(models.UserWorkoutCompletion).filter(
        models.UserWorkoutCompletion.user_id == current_user.id,
        models.UserWorkoutCompletion.workout_id == workout_id
    ).first()
    
    if not completion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must complete the workout before rating it"
        )
    
    # Update completion rating
    completion.enjoyment_rating = rating
    
    # Recalculate workout average rating
    workout = db.query(models.WorkoutOfTheDay).filter(
        models.WorkoutOfTheDay.id == workout_id
    ).first()
    
    if workout:
        all_ratings = db.query(models.UserWorkoutCompletion.enjoyment_rating).filter(
            models.UserWorkoutCompletion.workout_id == workout_id,
            models.UserWorkoutCompletion.enjoyment_rating.is_not(None)
        ).all()
        
        ratings = [r[0] for r in all_ratings]
        if ratings:
            workout.average_rating = sum(ratings) / len(ratings)
    
    db.commit()
    
    return {"message": "Rating saved successfully", "new_average": workout.average_rating}


@router.get("/weekly/schedule")
async def get_weekly_workout_schedule(
    week_offset: Optional[int] = Query(0, ge=-4, le=4),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weekly workout schedule"""
    # Calculate week start and end
    today = date.today()
    week_start = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    week_end = week_start + timedelta(days=6)
    
    # Get workouts for this week
    weekly_workouts = {}
    current_date = week_start
    
    while current_date <= week_end:
        # Get workout for this specific date
        workout = db.query(models.WorkoutOfTheDay).filter(
            models.WorkoutOfTheDay.date == current_date,
            models.WorkoutOfTheDay.is_active == True
        ).first()
        
        # Check if user completed workout on this date
        completion = db.query(models.UserWorkoutCompletion).filter(
            models.UserWorkoutCompletion.user_id == current_user.id,
            func.date(models.UserWorkoutCompletion.completed_at) == current_date
        ).first()
        
        weekly_workouts[current_date.isoformat()] = {
            "date": current_date.isoformat(),
            "day_name": current_date.strftime("%A"),
            "workout": workout,
            "completed": completion is not None,
            "completion_details": completion if completion else None
        }
        
        current_date += timedelta(days=1)
    
    return {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "workouts": weekly_workouts
    }