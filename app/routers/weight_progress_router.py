"""
Weight Progress router for weight tracking and loss progress
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from typing import List, Optional
from datetime import date, datetime, timedelta
import statistics
import os
import shutil

from app.database import get_db
from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/api/weight-progress", tags=["Weight Progress"])


@router.get("/entries", response_model=List[schemas.WeightEntryResponse])
async def get_weight_entries(
    limit: Optional[int] = Query(30, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's weight entries"""
    query = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id
    )
    
    if start_date:
        query = query.filter(models.WeightEntry.date >= start_date)
    if end_date:
        query = query.filter(models.WeightEntry.date <= end_date)
    
    entries = query.order_by(desc(models.WeightEntry.date)).limit(limit).all()
    
    # Calculate weight changes and averages
    for i, entry in enumerate(entries):
        if i < len(entries) - 1:
            previous_entry = entries[i + 1]
            entry.weight_change = entry.weight - previous_entry.weight
    
    return entries


@router.post("/entries", response_model=schemas.WeightEntryResponse)
async def create_weight_entry(
    entry: schemas.WeightEntryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new weight entry"""
    # Check if entry already exists for this date
    existing_entry = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id,
        models.WeightEntry.date == entry.date
    ).first()
    
    if existing_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight entry already exists for this date"
        )
    
    # Get previous entry to calculate weight change
    previous_entry = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id,
        models.WeightEntry.date < entry.date
    ).order_by(desc(models.WeightEntry.date)).first()
    
    # Create entry
    entry_data = entry.dict()
    entry_data["user_id"] = current_user.id
    
    if previous_entry:
        entry_data["weight_change"] = entry.weight - previous_entry.weight
    
    # Calculate weekly and monthly averages
    week_ago = entry.date - timedelta(days=7)
    month_ago = entry.date - timedelta(days=30)
    
    # Weekly average
    weekly_entries = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id,
        models.WeightEntry.date >= week_ago,
        models.WeightEntry.date <= entry.date
    ).all()
    
    if weekly_entries:
        entry_data["weekly_average"] = statistics.mean([e.weight for e in weekly_entries] + [entry.weight])
    
    # Monthly average
    monthly_entries = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id,
        models.WeightEntry.date >= month_ago,
        models.WeightEntry.date <= entry.date
    ).all()
    
    if monthly_entries:
        entry_data["monthly_average"] = statistics.mean([e.weight for e in monthly_entries] + [entry.weight])
    
    # Calculate progress toward goal
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if profile and profile.target_weight:
        starting_weight = current_user.weight or entry.weight
        total_to_lose = abs(starting_weight - profile.target_weight)
        if total_to_lose > 0:
            weight_lost = abs(starting_weight - entry.weight)
            entry_data["progress_toward_goal"] = min((weight_lost / total_to_lose) * 100, 100)
    
    db_entry = models.WeightEntry(**entry_data)
    db.add(db_entry)
    
    # Update user's current weight
    current_user.weight = entry.weight
    
    # Update profile current weight if exists
    if profile:
        profile.current_weight = entry.weight
    
    db.commit()
    db.refresh(db_entry)
    
    return db_entry


@router.get("/entries/{entry_id}", response_model=schemas.WeightEntryResponse)
async def get_weight_entry(
    entry_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific weight entry"""
    entry = db.query(models.WeightEntry).filter(
        models.WeightEntry.id == entry_id,
        models.WeightEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight entry not found"
        )
    
    return entry


@router.put("/entries/{entry_id}", response_model=schemas.WeightEntryResponse)
async def update_weight_entry(
    entry_id: int,
    entry_update: schemas.WeightEntryUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a weight entry"""
    entry = db.query(models.WeightEntry).filter(
        models.WeightEntry.id == entry_id,
        models.WeightEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight entry not found"
        )
    
    # Update entry
    update_data = entry_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)
    
    # Recalculate weight change if weight was updated
    if "weight" in update_data:
        previous_entry = db.query(models.WeightEntry).filter(
            models.WeightEntry.user_id == current_user.id,
            models.WeightEntry.date < entry.date
        ).order_by(desc(models.WeightEntry.date)).first()
        
        if previous_entry:
            entry.weight_change = entry.weight - previous_entry.weight
    
    db.commit()
    db.refresh(entry)
    
    return entry


@router.delete("/entries/{entry_id}")
async def delete_weight_entry(
    entry_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a weight entry"""
    entry = db.query(models.WeightEntry).filter(
        models.WeightEntry.id == entry_id,
        models.WeightEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight entry not found"
        )
    
    db.delete(entry)
    db.commit()
    
    return {"message": "Weight entry deleted successfully"}


@router.get("/summary", response_model=schemas.WeightProgressSummary)
async def get_weight_progress_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weight progress summary"""
    # Get recent entries
    recent_entries = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id
    ).order_by(desc(models.WeightEntry.date)).limit(10).all()
    
    if not recent_entries:
        return schemas.WeightProgressSummary(
            current_weight=current_user.weight or 0,
            recent_entries=[],
            trend="stable"
        )
    
    current_weight = recent_entries[0].weight
    starting_weight = current_user.weight if len(recent_entries) < 10 else recent_entries[-1].weight
    
    # Get target weight from profile
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    target_weight = profile.target_weight if profile else None
    
    # Calculate progress metrics
    total_weight_change = None
    weight_to_goal = None
    progress_percentage = None
    
    if starting_weight:
        total_weight_change = current_weight - starting_weight
        
        if target_weight:
            weight_to_goal = current_weight - target_weight
            total_to_lose = abs(starting_weight - target_weight)
            if total_to_lose > 0:
                weight_lost = abs(starting_weight - current_weight)
                progress_percentage = min((weight_lost / total_to_lose) * 100, 100)
    
    # Calculate averages
    last_7_entries = recent_entries[:7]
    last_30_entries = recent_entries
    
    weekly_average = statistics.mean([e.weight for e in last_7_entries]) if last_7_entries else None
    monthly_average = statistics.mean([e.weight for e in last_30_entries]) if last_30_entries else None
    
    # Determine trend
    trend = "stable"
    if len(recent_entries) >= 3:
        recent_weights = [e.weight for e in recent_entries[:3]]
        if recent_weights[0] > recent_weights[1] > recent_weights[2]:
            trend = "increasing"
        elif recent_weights[0] < recent_weights[1] < recent_weights[2]:
            trend = "decreasing"
    
    return schemas.WeightProgressSummary(
        current_weight=current_weight,
        starting_weight=starting_weight,
        target_weight=target_weight,
        total_weight_change=total_weight_change,
        weight_to_goal=weight_to_goal,
        progress_percentage=progress_percentage,
        recent_entries=recent_entries,
        weekly_average=weekly_average,
        monthly_average=monthly_average,
        trend=trend
    )


@router.get("/analytics/trends")
async def get_weight_trends(
    days: Optional[int] = Query(30, ge=7, le=365),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weight trends and analytics"""
    start_date = date.today() - timedelta(days=days)
    
    entries = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id,
        models.WeightEntry.date >= start_date
    ).order_by(models.WeightEntry.date).all()
    
    if not entries:
        return {"message": "No data available for the specified period"}
    
    # Calculate various metrics
    weights = [e.weight for e in entries]
    dates = [e.date.isoformat() for e in entries]
    
    # Weight change over period
    total_change = weights[-1] - weights[0] if len(weights) > 1 else 0
    
    # Average weekly change
    weekly_changes = []
    for i in range(7, len(weights), 7):
        week_change = weights[i] - weights[i-7]
        weekly_changes.append(week_change)
    
    avg_weekly_change = statistics.mean(weekly_changes) if weekly_changes else 0
    
    # Volatility (standard deviation)
    volatility = statistics.stdev(weights) if len(weights) > 1 else 0
    
    # Consistency score (based on how close to target trend)
    consistency_score = max(0, 100 - (volatility * 10))
    
    # Projection (simple linear regression)
    if len(entries) >= 7:
        x_values = list(range(len(weights)))
        y_values = weights
        
        # Simple linear regression
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        # Project 30 days ahead
        future_weight = slope * (len(weights) + 30) + intercept
    else:
        future_weight = weights[-1] if weights else 0
    
    return {
        "period_days": days,
        "total_entries": len(entries),
        "weight_data": {
            "dates": dates,
            "weights": weights
        },
        "metrics": {
            "total_change": round(total_change, 2),
            "average_weekly_change": round(avg_weekly_change, 2),
            "volatility": round(volatility, 2),
            "consistency_score": round(consistency_score, 2),
            "current_weight": weights[-1] if weights else 0,
            "highest_weight": max(weights) if weights else 0,
            "lowest_weight": min(weights) if weights else 0
        },
        "projections": {
            "30_day_projection": round(future_weight, 2),
            "trend_direction": "decreasing" if avg_weekly_change < -0.1 else "increasing" if avg_weekly_change > 0.1 else "stable"
        }
    }


@router.post("/entries/{entry_id}/upload-photo")
async def upload_progress_photo(
    entry_id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload progress photo for a weight entry"""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Check if entry exists and belongs to user
    entry = db.query(models.WeightEntry).filter(
        models.WeightEntry.id == entry_id,
        models.WeightEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight entry not found"
        )
    
    # Create uploads directory
    upload_dir = "uploads/progress_photos"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"progress_{current_user.id}_{entry_id}_{int(datetime.now().timestamp())}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update entry with photo URL
    entry.progress_photo_url = f"/{file_path}"
    db.commit()
    
    return {"message": "Progress photo uploaded successfully", "url": f"/{file_path}"}


@router.get("/goals")
async def get_weight_related_goals(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weight-related goals"""
    goals = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.category == "weight_loss"
    ).all()
    
    return goals


@router.get("/milestones")
async def get_weight_milestones(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weight loss milestones achieved"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile or not profile.target_weight:
        return {"milestones": []}
    
    # Get all weight entries
    entries = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id
    ).order_by(models.WeightEntry.date).all()
    
    if not entries:
        return {"milestones": []}
    
    starting_weight = current_user.weight or entries[0].weight
    target_weight = profile.target_weight
    total_to_lose = abs(starting_weight - target_weight)
    
    milestones = []
    milestone_percentages = [10, 25, 50, 75, 90, 100]
    
    for percentage in milestone_percentages:
        milestone_weight = starting_weight - (total_to_lose * percentage / 100)
        
        # Find if this milestone was reached
        reached_entry = None
        for entry in entries:
            if (starting_weight > target_weight and entry.weight <= milestone_weight) or \
               (starting_weight < target_weight and entry.weight >= milestone_weight):
                reached_entry = entry
                break
        
        milestones.append({
            "percentage": percentage,
            "target_weight": round(milestone_weight, 1),
            "reached": reached_entry is not None,
            "date_reached": reached_entry.date.isoformat() if reached_entry else None,
            "title": f"{percentage}% of goal reached"
        })
    
    return {"milestones": milestones}


@router.get("/weekly-summary")
async def get_weekly_weight_summary(
    weeks_back: Optional[int] = Query(4, ge=1, le=12),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weekly weight summary"""
    end_date = date.today()
    start_date = end_date - timedelta(weeks=weeks_back)
    
    entries = db.query(models.WeightEntry).filter(
        models.WeightEntry.user_id == current_user.id,
        models.WeightEntry.date >= start_date
    ).order_by(models.WeightEntry.date).all()
    
    # Group by week
    weekly_data = []
    current_week_start = start_date
    
    while current_week_start <= end_date:
        week_end = current_week_start + timedelta(days=6)
        
        week_entries = [
            e for e in entries 
            if current_week_start <= e.date <= week_end
        ]
        
        if week_entries:
            avg_weight = statistics.mean([e.weight for e in week_entries])
            start_weight = week_entries[0].weight
            end_weight = week_entries[-1].weight
            weight_change = end_weight - start_weight
        else:
            avg_weight = 0
            weight_change = 0
        
        weekly_data.append({
            "week_start": current_week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "entries_count": len(week_entries),
            "average_weight": round(avg_weight, 2) if avg_weight else 0,
            "weight_change": round(weight_change, 2) if week_entries else 0,
            "consistency": len(week_entries) / 7 * 100  # percentage of days logged
        })
        
        current_week_start += timedelta(weeks=1)
    
    return {"weekly_data": weekly_data}