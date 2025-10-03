"""
Motivation router - handles daily motivation system, quotes, challenges, streaks, and rewards
"""
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, asc, or_
from slowapi import Limiter
from slowapi.util import get_remote_address
import random

from app.database import get_db
from app import models, schemas
from app.schemas import (
    DailyQuoteResponse, DailyChallengeResponse,
    UserDailyChallengeLogCreate, UserDailyChallengeLogResponse, UserDailyChallengeLogUpdate,
    UserStreakResponse, UserMotivationStatsResponse, UserMotivationStatsUpdate,
    UserMotivationRewardResponse, MotivationLevelResponse,
    DailyMotivationSummary, MotivationDashboard,
    MessageResponse
)
from app.security import get_current_user

router = APIRouter(prefix="/api/motivation", tags=["Motivación Diaria"])
limiter = Limiter(key_func=get_remote_address)


# Daily Quote Endpoints
@router.get("/quote/daily", response_model=DailyQuoteResponse)
async def get_daily_quote(
    category: Optional[str] = Query(None, description="Categoría del quote"),
    language: str = Query("es", pattern="^(es|en)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener quote motivacional del día"""
    # Update user stats for viewing daily quote
    await update_user_motivation_stats(
        user_id=current_user.id,
        db=db,
        daily_quote_viewed=True
    )
    
    # Get random quote based on criteria
    query = db.query(models.DailyQuote).filter(
        and_(
            models.DailyQuote.is_active == True,
            models.DailyQuote.language == language
        )
    )
    
    if category:
        query = query.filter(models.DailyQuote.category == category)
    
    quotes = query.all()
    if not quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay quotes disponibles para los criterios especificados"
        )
    
    # Return random quote
    return random.choice(quotes)


@router.get("/quotes", response_model=List[DailyQuoteResponse])
async def get_quotes(
    category: Optional[str] = Query(None),
    language: str = Query("es", pattern="^(es|en)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener lista de quotes motivacionales"""
    query = db.query(models.DailyQuote).filter(
        and_(
            models.DailyQuote.is_active == True,
            models.DailyQuote.language == language
        )
    )
    
    if category:
        query = query.filter(models.DailyQuote.category == category)
    
    quotes = query.order_by(func.random()).offset(skip).limit(limit).all()
    return quotes


# Daily Challenge Endpoints
@router.get("/challenge/daily", response_model=DailyChallengeResponse)
async def get_daily_challenge(
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$"),
    category: Optional[str] = Query(None, pattern="^(cardio|strength|flexibility|mindfulness|nutrition)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener desafío diario personalizado"""
    # Check if user already has a challenge for today
    today = date.today()
    existing_challenge = db.query(models.UserDailyChallengeLog).filter(
        and_(
            models.UserDailyChallengeLog.user_id == current_user.id,
            models.UserDailyChallengeLog.date == today
        )
    ).first()
    
    if existing_challenge:
        return existing_challenge.challenge
    
    # Get available challenges based on criteria
    query = db.query(models.DailyChallenge).filter(models.DailyChallenge.is_active == True)
    
    if difficulty:
        query = query.filter(models.DailyChallenge.difficulty_level == difficulty)
    if category:
        query = query.filter(models.DailyChallenge.category == category)
    
    challenges = query.all()
    if not challenges:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay desafíos disponibles para los criterios especificados"
        )
    
    # Return random challenge
    return random.choice(challenges)


@router.post("/challenge/accept", response_model=UserDailyChallengeLogResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def accept_daily_challenge(
    request: Request,
    challenge_log: UserDailyChallengeLogCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Aceptar desafío diario"""
    # Check if user already accepted a challenge today
    existing_log = db.query(models.UserDailyChallengeLog).filter(
        and_(
            models.UserDailyChallengeLog.user_id == current_user.id,
            models.UserDailyChallengeLog.date == challenge_log.date
        )
    ).first()
    
    if existing_log:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya has aceptado un desafío para esta fecha"
        )
    
    # Validate challenge exists
    challenge = db.query(models.DailyChallenge).filter(
        models.DailyChallenge.id == challenge_log.challenge_id
    ).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafío no encontrado"
        )
    
    db_log = models.UserDailyChallengeLog(
        user_id=current_user.id,
        **challenge_log.dict()
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    # Update user stats
    await update_user_motivation_stats(
        user_id=current_user.id,
        db=db,
        daily_challenge_accepted=True
    )
    
    # Update streaks in background
    background_tasks.add_task(update_user_streaks, current_user.id, "challenge", db)
    
    return db_log


@router.put("/challenge/{log_id}", response_model=UserDailyChallengeLogResponse)
async def update_challenge_log(
    log_id: int,
    log_data: UserDailyChallengeLogUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Actualizar log de desafío diario"""
    log = db.query(models.UserDailyChallengeLog).filter(
        and_(
            models.UserDailyChallengeLog.id == log_id,
            models.UserDailyChallengeLog.user_id == current_user.id
        )
    ).first()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log de desafío no encontrado"
        )
    
    # Update only provided fields
    update_data = log_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(log, field, value)
    
    # If challenge is being completed, award points and update stats
    if log_data.status == "completed" and log.status != "completed":
        challenge = db.query(models.DailyChallenge).filter(
            models.DailyChallenge.id == log.challenge_id
        ).first()
        
        if challenge:
            log.points_earned = challenge.points_reward
            log.completed_at = datetime.now()
            
            # Update user stats
            await update_user_motivation_stats(
                user_id=current_user.id,
                db=db,
                daily_challenge_completed=True,
                daily_points_earned=challenge.points_reward
            )
            
            # Check for rewards in background
            background_tasks.add_task(check_motivation_rewards, current_user.id, db)
    
    db.commit()
    db.refresh(log)
    
    return log


@router.get("/challenges/my-logs", response_model=List[UserDailyChallengeLogResponse])
async def get_my_challenge_logs(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None, pattern="^(started|completed|skipped|failed)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener historial de desafíos del usuario"""
    query = db.query(models.UserDailyChallengeLog).filter(
        models.UserDailyChallengeLog.user_id == current_user.id
    )
    
    if start_date:
        query = query.filter(models.UserDailyChallengeLog.date >= start_date)
    if end_date:
        query = query.filter(models.UserDailyChallengeLog.date <= end_date)
    if status:
        query = query.filter(models.UserDailyChallengeLog.status == status)
    
    logs = query.order_by(desc(models.UserDailyChallengeLog.date)).offset(skip).limit(limit).all()
    return logs


# Streaks Endpoints
@router.get("/streaks", response_model=List[UserStreakResponse])
async def get_user_streaks(
    streak_type: Optional[str] = Query(None, pattern="^(workout|challenge|login|progress_update)$"),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener streaks del usuario"""
    query = db.query(models.UserStreak).filter(
        models.UserStreak.user_id == current_user.id
    )
    
    if streak_type:
        query = query.filter(models.UserStreak.streak_type == streak_type)
    if active_only:
        query = query.filter(models.UserStreak.is_active == True)
    
    streaks = query.order_by(desc(models.UserStreak.current_count)).all()
    return streaks


@router.post("/streaks/update", response_model=MessageResponse)
@limiter.limit("20/minute")
async def update_streak(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    streak_type: str = Query(..., pattern="^(workout|challenge|login|progress_update)$")
):
    """Actualizar streak del usuario"""
    background_tasks.add_task(update_user_streaks, current_user.id, streak_type, db)
    return {"message": f"Streak de {streak_type} actualizado"}


# Motivation Stats Endpoints
@router.get("/stats/today", response_model=UserMotivationStatsResponse)
async def get_today_motivation_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener estadísticas de motivación de hoy"""
    today = date.today()
    stats = db.query(models.UserMotivationStats).filter(
        and_(
            models.UserMotivationStats.user_id == current_user.id,
            models.UserMotivationStats.date == today
        )
    ).first()
    
    if not stats:
        # Create today's stats if they don't exist
        stats = models.UserMotivationStats(
            user_id=current_user.id,
            date=today
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats


@router.put("/stats/today", response_model=UserMotivationStatsResponse)
async def update_today_motivation_stats(
    stats_data: UserMotivationStatsUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Actualizar estadísticas de motivación de hoy"""
    today = date.today()
    stats = db.query(models.UserMotivationStats).filter(
        and_(
            models.UserMotivationStats.user_id == current_user.id,
            models.UserMotivationStats.date == today
        )
    ).first()
    
    if not stats:
        stats = models.UserMotivationStats(
            user_id=current_user.id,
            date=today
        )
        db.add(stats)
    
    # Update only provided fields
    update_data = stats_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(stats, field):
            setattr(stats, field, value)
    
    # Recalculate motivation score
    stats.motivation_score = calculate_motivation_score(stats)
    
    db.commit()
    db.refresh(stats)
    
    return stats


# Rewards and Levels Endpoints
@router.get("/rewards", response_model=List[UserMotivationRewardResponse])
async def get_user_rewards(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener recompensas del usuario"""
    rewards = db.query(models.UserMotivationReward).filter(
        models.UserMotivationReward.user_id == current_user.id
    ).order_by(desc(models.UserMotivationReward.earned_at)).offset(skip).limit(limit).all()
    
    return rewards


@router.get("/level", response_model=MotivationLevelResponse)
async def get_user_motivation_level(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener nivel de motivación actual del usuario"""
    # Calculate total points
    total_points = calculate_user_total_points(current_user.id, db)
    
    # Find current level
    level = db.query(models.MotivationLevel).filter(
        and_(
            models.MotivationLevel.min_points <= total_points,
            or_(
                models.MotivationLevel.max_points >= total_points,
                models.MotivationLevel.max_points.is_(None)
            )
        )
    ).order_by(desc(models.MotivationLevel.level_number)).first()
    
    if not level:
        # Return default level if no levels configured
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay niveles de motivación configurados"
        )
    
    return level


# Dashboard and Summary Endpoints
@router.get("/dashboard", response_model=MotivationDashboard)
async def get_motivation_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener dashboard completo de motivación"""
    # Get user level
    total_points = calculate_user_total_points(current_user.id, db)
    user_level = db.query(models.MotivationLevel).filter(
        and_(
            models.MotivationLevel.min_points <= total_points,
            or_(
                models.MotivationLevel.max_points >= total_points,
                models.MotivationLevel.max_points.is_(None)
            )
        )
    ).order_by(desc(models.MotivationLevel.level_number)).first()
    
    # Get active streaks
    active_streaks = db.query(models.UserStreak).filter(
        and_(
            models.UserStreak.user_id == current_user.id,
            models.UserStreak.is_active == True
        )
    ).all()
    
    # Get recent challenges (last 7 days)
    week_ago = date.today() - timedelta(days=7)
    recent_challenges = db.query(models.UserDailyChallengeLog).filter(
        and_(
            models.UserDailyChallengeLog.user_id == current_user.id,
            models.UserDailyChallengeLog.date >= week_ago
        )
    ).order_by(desc(models.UserDailyChallengeLog.date)).limit(10).all()
    
    # Get earned rewards (last 30 days)
    month_ago = datetime.now() - timedelta(days=30)
    earned_rewards = db.query(models.UserMotivationReward).filter(
        and_(
            models.UserMotivationReward.user_id == current_user.id,
            models.UserMotivationReward.earned_at >= month_ago
        )
    ).order_by(desc(models.UserMotivationReward.earned_at)).limit(10).all()
    
    # Get weekly stats
    weekly_stats = db.query(models.UserMotivationStats).filter(
        and_(
            models.UserMotivationStats.user_id == current_user.id,
            models.UserMotivationStats.date >= week_ago
        )
    ).order_by(asc(models.UserMotivationStats.date)).all()
    
    # Calculate motivation trend
    motivation_trend = calculate_motivation_trend(weekly_stats)
    
    # Calculate consistency score
    consistency_score = calculate_consistency_score(weekly_stats)
    
    return MotivationDashboard(
        user_level=user_level,
        total_points=total_points,
        active_streaks=active_streaks,
        recent_challenges=recent_challenges,
        earned_rewards=earned_rewards,
        weekly_stats=weekly_stats,
        motivation_trend=motivation_trend,
        consistency_score=consistency_score
    )


@router.get("/summary/daily", response_model=DailyMotivationSummary)
async def get_daily_motivation_summary(
    target_date: Optional[date] = Query(None, description="Fecha específica (default: hoy)"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Obtener resumen de motivación diaria"""
    if not target_date:
        target_date = date.today()
    
    # Get daily quote
    daily_quote = await get_daily_quote(db=db, current_user=current_user)
    
    # Get suggested challenge
    suggested_challenge = await get_daily_challenge(db=db, current_user=current_user)
    
    # Get current streaks
    current_streaks = await get_user_streaks(active_only=True, db=db, current_user=current_user)
    
    # Get motivation stats for the date
    motivation_stats = db.query(models.UserMotivationStats).filter(
        and_(
            models.UserMotivationStats.user_id == current_user.id,
            models.UserMotivationStats.date == target_date
        )
    ).first()
    
    if not motivation_stats:
        motivation_stats = models.UserMotivationStats(
            user_id=current_user.id,
            date=target_date
        )
        db.add(motivation_stats)
        db.commit()
        db.refresh(motivation_stats)
    
    # Get current level
    current_level = await get_user_motivation_level(db=db, current_user=current_user)
    
    # Calculate points to next level
    total_points = calculate_user_total_points(current_user.id, db)
    next_level = db.query(models.MotivationLevel).filter(
        models.MotivationLevel.level_number > current_level.level_number
    ).order_by(asc(models.MotivationLevel.level_number)).first()
    
    points_to_next_level = next_level.min_points - total_points if next_level else 0
    
    # Get recent rewards (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_rewards = db.query(models.UserMotivationReward).filter(
        and_(
            models.UserMotivationReward.user_id == current_user.id,
            models.UserMotivationReward.earned_at >= week_ago
        )
    ).order_by(desc(models.UserMotivationReward.earned_at)).limit(5).all()
    
    return DailyMotivationSummary(
        date=target_date.isoformat(),
        daily_quote=daily_quote,
        suggested_challenge=suggested_challenge,
        current_streaks=current_streaks,
        motivation_stats=motivation_stats,
        current_level=current_level,
        points_to_next_level=points_to_next_level,
        recent_rewards=recent_rewards
    )


# Helper Functions
async def update_user_motivation_stats(user_id: int, db: Session, **kwargs):
    """Update user motivation stats for today"""
    today = date.today()
    stats = db.query(models.UserMotivationStats).filter(
        and_(
            models.UserMotivationStats.user_id == user_id,
            models.UserMotivationStats.date == today
        )
    ).first()
    
    if not stats:
        stats = models.UserMotivationStats(
            user_id=user_id,
            date=today
        )
        db.add(stats)
    
    # Update provided fields
    for field, value in kwargs.items():
        if hasattr(stats, field):
            if field == "daily_points_earned":
                stats.daily_points_earned += value
            else:
                setattr(stats, field, value)
    
    # Recalculate motivation score
    stats.motivation_score = calculate_motivation_score(stats)
    
    db.commit()


async def update_user_streaks(user_id: int, streak_type: str, db: Session):
    """Update user streaks"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    streak = db.query(models.UserStreak).filter(
        and_(
            models.UserStreak.user_id == user_id,
            models.UserStreak.streak_type == streak_type
        )
    ).first()
    
    if not streak:
        streak = models.UserStreak(
            user_id=user_id,
            streak_type=streak_type,
            current_count=1,
            longest_streak=1,
            last_activity_date=today,
            started_at=today
        )
        db.add(streak)
    else:
        # Check if streak continues
        if streak.last_activity_date == yesterday:
            streak.current_count += 1
            streak.longest_streak = max(streak.longest_streak, streak.current_count)
        elif streak.last_activity_date != today:
            # Streak broken, restart
            streak.current_count = 1
            streak.started_at = today
            streak.streak_broken_at = datetime.now()
        
        streak.last_activity_date = today
        streak.is_active = True
    
    db.commit()


async def check_motivation_rewards(user_id: int, db: Session):
    """Check and award motivation rewards"""
    # Calculate various user metrics
    total_points = calculate_user_total_points(user_id, db)
    total_challenges = db.query(models.UserDailyChallengeLog).filter(
        and_(
            models.UserDailyChallengeLog.user_id == user_id,
            models.UserDailyChallengeLog.status == "completed"
        )
    ).count()
    
    # Get longest streaks
    longest_workout_streak = db.query(models.UserStreak).filter(
        and_(
            models.UserStreak.user_id == user_id,
            models.UserStreak.streak_type == "workout"
        )
    ).first()
    
    workout_streak_days = longest_workout_streak.longest_streak if longest_workout_streak else 0
    
    # Check available rewards
    available_rewards = db.query(models.MotivationReward).filter(
        models.MotivationReward.is_active == True
    ).all()
    
    for reward in available_rewards:
        # Check if user already has this reward
        existing_reward = db.query(models.UserMotivationReward).filter(
            and_(
                models.UserMotivationReward.user_id == user_id,
                models.UserMotivationReward.reward_id == reward.id
            )
        ).first()
        
        if existing_reward:
            continue
        
        # Check if user qualifies for this reward
        qualifies = False
        achievement_value = 0
        
        if reward.requirement_type == "total_points" and total_points >= reward.requirement_value:
            qualifies = True
            achievement_value = total_points
        elif reward.requirement_type == "challenges_completed" and total_challenges >= reward.requirement_value:
            qualifies = True
            achievement_value = total_challenges
        elif reward.requirement_type == "streak_days" and workout_streak_days >= reward.requirement_value:
            qualifies = True
            achievement_value = workout_streak_days
        
        if qualifies:
            # Award the reward
            user_reward = models.UserMotivationReward(
                user_id=user_id,
                reward_id=reward.id,
                achievement_value=achievement_value
            )
            db.add(user_reward)
            
            # Create notification
            notification = models.Notification(
                user_id=user_id,
                title="🏆 ¡Nueva Recompensa Desbloqueada!",
                body=f"Has ganado: {reward.name}",
                notification_type="achievement",
                category="motivation",
                data={
                    "reward_id": reward.id,
                    "reward_name": reward.name,
                    "achievement_value": achievement_value
                }
            )
            db.add(notification)
    
    db.commit()


def calculate_motivation_score(stats: models.UserMotivationStats) -> float:
    """Calculate daily motivation score (0-100)"""
    score = 0.0
    
    if stats.daily_quote_viewed:
        score += 10
    if stats.daily_challenge_accepted:
        score += 20
    if stats.daily_challenge_completed:
        score += 30
    if stats.progress_logged:
        score += 15
    
    # Bonus for workouts
    score += min(stats.workouts_completed * 10, 25)
    
    return min(score, 100.0)


def calculate_user_total_points(user_id: int, db: Session) -> int:
    """Calculate user's total motivation points"""
    total_points = db.query(func.sum(models.UserMotivationStats.daily_points_earned)).filter(
        models.UserMotivationStats.user_id == user_id
    ).scalar()
    
    return total_points or 0


def calculate_motivation_trend(weekly_stats: List[models.UserMotivationStats]) -> str:
    """Calculate motivation trend based on weekly stats"""
    if len(weekly_stats) < 2:
        return "stable"
    
    # Compare recent days with earlier days
    recent_avg = sum(stat.motivation_score for stat in weekly_stats[-3:]) / len(weekly_stats[-3:])
    earlier_avg = sum(stat.motivation_score for stat in weekly_stats[:3]) / len(weekly_stats[:3])
    
    if recent_avg > earlier_avg + 5:
        return "increasing"
    elif recent_avg < earlier_avg - 5:
        return "decreasing"
    else:
        return "stable"


def calculate_consistency_score(weekly_stats: List[models.UserMotivationStats]) -> float:
    """Calculate consistency score based on weekly activity"""
    if not weekly_stats:
        return 0.0
    
    active_days = sum(1 for stat in weekly_stats if stat.motivation_score > 20)
    total_days = len(weekly_stats)
    
    return (active_days / total_days) * 100