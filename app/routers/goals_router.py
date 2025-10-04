"""
Goals router for fitness goals management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional
from datetime import date, datetime, timedelta

from app.database import get_db
from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/api/goals", tags=["Goals"])


@router.get("/", response_model=List[schemas.GoalResponse])
async def get_my_goals(
    status_filter: Optional[str] = Query(None, pattern="^(active|completed|paused|cancelled)$"),
    category_filter: Optional[str] = Query(None, pattern="^(weight_loss|muscle_gain|strength|endurance|nutrition|habits)$"),
    priority_filter: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    sort_by: Optional[str] = Query("created_at", pattern="^(created_at|target_date|priority|progress_percentage)$"),
    sort_order: Optional[str] = Query("desc", pattern="^(asc|desc)$"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's goals with filtering and sorting"""
    query = db.query(models.Goal).filter(models.Goal.user_id == current_user.id)
    
    # Apply filters
    if status_filter:
        query = query.filter(models.Goal.status == status_filter)
    if category_filter:
        query = query.filter(models.Goal.category == category_filter)
    if priority_filter:
        query = query.filter(models.Goal.priority == priority_filter)
    
    # Apply sorting
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.Goal, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.Goal, sort_by)))
    
    goals = query.all()
    
    # Calculate progress percentages and update estimated completion dates
    for goal in goals:
        if goal.target_value > 0:
            goal.progress_percentage = min((goal.current_value / goal.target_value) * 100, 100)
        else:
            goal.progress_percentage = 0
    
    return goals


@router.post("/", response_model=schemas.GoalResponse)
async def create_goal(
    goal: schemas.GoalCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new fitness goal"""
    goal_data = goal.dict()
    goal_data["user_id"] = current_user.id
    goal_data["start_date"] = goal_data.get("start_date", date.today())
    
    # Calculate initial progress percentage
    if goal_data["target_value"] > 0:
        starting_value = goal_data.get("starting_value", 0)
        goal_data["current_value"] = starting_value
        goal_data["progress_percentage"] = (starting_value / goal_data["target_value"]) * 100
    
    # Determine if it's a SMART goal
    goal_data["is_smart_goal"] = all([
        goal_data.get("title"),
        goal_data.get("target_value"),
        goal_data.get("unit"),
        goal_data.get("target_date"),
        goal_data.get("motivation_reason")
    ])
    
    # Calculate estimated completion date based on current progress
    if goal_data.get("target_date") and goal_data["target_value"] > 0:
        goal_data["estimated_completion_date"] = goal_data["target_date"]
    
    db_goal = models.Goal(**goal_data)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    
    return db_goal


@router.get("/{goal_id}", response_model=schemas.GoalResponse)
async def get_goal(
    goal_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific goal by ID"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    # Update progress percentage
    if goal.target_value > 0:
        goal.progress_percentage = min((goal.current_value / goal.target_value) * 100, 100)
    
    return goal


@router.put("/{goal_id}", response_model=schemas.GoalResponse)
async def update_goal(
    goal_id: int,
    goal_update: schemas.GoalUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a goal"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    # Update goal with provided data
    update_data = goal_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    # Recalculate progress percentage if target_value changed
    if "target_value" in update_data or "current_value" in update_data:
        if goal.target_value > 0:
            goal.progress_percentage = min((goal.current_value / goal.target_value) * 100, 100)
            
            # Check if goal is completed
            if goal.progress_percentage >= 100 and goal.status == "active":
                goal.status = "completed"
    
    goal.last_updated_progress = date.today()
    db.commit()
    db.refresh(goal)
    
    return goal


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a goal"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    db.delete(goal)
    db.commit()
    
    return {"message": "Goal deleted successfully"}


@router.post("/{goal_id}/progress", response_model=schemas.GoalProgressResponse)
async def log_goal_progress(
    goal_id: int,
    progress: schemas.GoalProgressCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log progress for a goal"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    # Create progress entry
    progress_data = progress.dict()
    progress_data["goal_id"] = goal_id
    progress_data["date"] = date.today()
    
    # Calculate progress change
    previous_value = goal.current_value
    progress_data["progress_change"] = progress_data["progress_value"] - previous_value
    
    # Calculate progress percentage
    if goal.target_value > 0:
        progress_data["progress_percentage"] = min((progress_data["progress_value"] / goal.target_value) * 100, 100)
    else:
        progress_data["progress_percentage"] = 0
    
    db_progress = models.GoalProgress(**progress_data)
    db.add(db_progress)
    
    # Update goal's current value and progress
    goal.current_value = progress_data["progress_value"]
    goal.progress_percentage = progress_data["progress_percentage"]
    goal.last_updated_progress = date.today()
    
    # Check if goal is completed
    if goal.progress_percentage >= 100 and goal.status == "active":
        goal.status = "completed"
    
    db.commit()
    db.refresh(db_progress)
    
    return db_progress


@router.get("/{goal_id}/progress", response_model=List[schemas.GoalProgressResponse])
async def get_goal_progress_history(
    goal_id: int,
    limit: Optional[int] = Query(30, ge=1, le=100),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress history for a goal"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    progress_entries = db.query(models.GoalProgress).filter(
        models.GoalProgress.goal_id == goal_id
    ).order_by(desc(models.GoalProgress.date)).limit(limit).all()
    
    return progress_entries


@router.get("/categories/stats")
async def get_goals_by_category_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics of goals by category"""
    from sqlalchemy import func
    
    stats = db.query(
        models.Goal.category,
        func.count(models.Goal.id).label("total"),
        func.count(models.Goal.id).filter(models.Goal.status == "active").label("active"),
        func.count(models.Goal.id).filter(models.Goal.status == "completed").label("completed"),
        func.avg(models.Goal.progress_percentage).label("avg_progress")
    ).filter(
        models.Goal.user_id == current_user.id
    ).group_by(models.Goal.category).all()
    
    return [
        {
            "category": stat.category,
            "total": stat.total,
            "active": stat.active,
            "completed": stat.completed,
            "average_progress": round(stat.avg_progress or 0, 2)
        }
        for stat in stats
    ]


@router.get("/dashboard/summary")
async def get_goals_dashboard_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get goals dashboard summary"""
    # Get active goals
    active_goals = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.status == "active"
    ).all()
    
    # Get completed goals this month
    start_of_month = date.today().replace(day=1)
    completed_this_month = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.status == "completed",
        models.Goal.updated_at >= start_of_month
    ).count()
    
    # Get overdue goals
    overdue_goals = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.status == "active",
        models.Goal.target_date < date.today()
    ).count()
    
    # Calculate average progress
    total_progress = sum(goal.progress_percentage for goal in active_goals)
    avg_progress = total_progress / len(active_goals) if active_goals else 0
    
    # Get upcoming deadlines (next 7 days)
    upcoming_deadline = date.today() + timedelta(days=7)
    upcoming_goals = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.status == "active",
        models.Goal.target_date.between(date.today(), upcoming_deadline)
    ).all()
    
    return {
        "total_active_goals": len(active_goals),
        "completed_this_month": completed_this_month,
        "overdue_goals": overdue_goals,
        "average_progress": round(avg_progress, 2),
        "upcoming_deadlines": len(upcoming_goals),
        "most_progressed_goal": max(active_goals, key=lambda g: g.progress_percentage) if active_goals else None,
        "urgent_goals": [goal for goal in active_goals if goal.priority in ["high", "critical"]],
        "recent_activity": len([goal for goal in active_goals if goal.last_updated_progress and goal.last_updated_progress >= date.today() - timedelta(days=7)])
    }


@router.post("/{goal_id}/milestone")
async def add_goal_milestone(
    goal_id: int,
    milestone_title: str,
    milestone_value: float,
    milestone_date: Optional[date] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a milestone to a goal"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    # Add milestone to goal's milestones
    if not goal.milestones:
        goal.milestones = []
    
    milestone = {
        "title": milestone_title,
        "value": milestone_value,
        "target_date": milestone_date.isoformat() if milestone_date else None,
        "created_at": datetime.now().isoformat()
    }
    
    goal.milestones.append(milestone)
    db.commit()
    
    return {"message": "Milestone added successfully", "milestone": milestone}


@router.put("/{goal_id}/milestone/{milestone_index}/complete")
async def complete_goal_milestone(
    goal_id: int,
    milestone_index: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a milestone as completed"""
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    if not goal.milestones or milestone_index >= len(goal.milestones):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milestone not found"
        )
    
    # Add to achieved milestones
    if not goal.milestones_achieved:
        goal.milestones_achieved = []
    
    milestone = goal.milestones[milestone_index]
    milestone["completed_at"] = datetime.now().isoformat()
    goal.milestones_achieved.append(milestone)
    
    db.commit()
    
    return {"message": "Milestone completed successfully"}