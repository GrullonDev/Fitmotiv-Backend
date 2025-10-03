"""
Pydantic schemas for request/response DTOs
"""
from typing import Optional, Dict, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date


# Base schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=13, le=120)
    height: Optional[int] = Field(None, ge=100, le=250)  # cm
    weight: Optional[int] = Field(None, ge=30, le=300)   # kg
    fitness_goal: Optional[str] = Field(None, pattern="^(lose_weight|gain_muscle|maintain|improve_endurance|general_fitness)$")
    activity_level: Optional[str] = Field(None, pattern="^(sedentary|light|moderate|active|very_active)$")
    bio: Optional[str] = Field(None, max_length=500)


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user updates"""
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=13, le=120)
    height: Optional[int] = Field(None, ge=100, le=250)
    weight: Optional[int] = Field(None, ge=30, le=300)
    fitness_goal: Optional[str] = Field(None, pattern="^(lose_weight|gain_muscle|maintain|improve_endurance|general_fitness)$")
    activity_level: Optional[str] = Field(None, pattern="^(sedentary|light|moderate|active|very_active)$")
    bio: Optional[str] = Field(None, max_length=500)


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserInDB(UserResponse):
    """Schema for user in database (includes hashed password)"""
    hashed_password: str


# Authentication schemas
class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str = Field(..., description="Username or email")
    password: str


class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


# Response schemas
class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str


# Enhanced Authentication schemas
class TokenRefresh(BaseModel):
    """Token refresh schema"""
    refresh_token: str
    access_token: Optional[str] = None


class Token(BaseModel):
    """Enhanced token response schema"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr


class PasswordReset(BaseModel):
    """Password reset schema"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class EmailVerification(BaseModel):
    """Email verification schema"""
    token: str


# Exercise schemas
class ExerciseBase(BaseModel):
    """Base exercise schema"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    category: str = Field(..., pattern="^(strength|cardio|flexibility|balance)$")
    muscle_groups: Optional[list] = None
    equipment_needed: Optional[list] = None
    difficulty_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    instructions: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    """Schema for exercise creation"""
    pass


class ExerciseUpdate(BaseModel):
    """Schema for exercise update"""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, pattern="^(strength|cardio|flexibility|balance)$")
    muscle_groups: Optional[list] = None
    equipment_needed: Optional[list] = None
    difficulty_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    instructions: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    """Schema for exercise response"""
    id: int
    is_custom: bool
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


# Routine schemas
class RoutineExerciseBase(BaseModel):
    """Base routine exercise schema"""
    exercise_id: int
    order_in_routine: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration_seconds: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None


class RoutineExerciseCreate(RoutineExerciseBase):
    """Schema for routine exercise creation"""
    pass


class RoutineExerciseUpdate(BaseModel):
    """Schema for routine exercise update"""
    order_in_routine: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration_seconds: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None


class RoutineExerciseResponse(RoutineExerciseBase):
    """Schema for routine exercise response"""
    id: int
    exercise: ExerciseResponse

    class Config:
        orm_mode = True


class RoutineBase(BaseModel):
    """Base routine schema"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    difficulty_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    duration_minutes: Optional[int] = None
    category: Optional[str] = None
    is_public: bool = False
    is_favorite: bool = False


class RoutineCreate(RoutineBase):
    """Schema for routine creation"""
    exercises: Optional[list[RoutineExerciseCreate]] = []


class RoutineUpdate(BaseModel):
    """Schema for routine update"""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    difficulty_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    duration_minutes: Optional[int] = None
    category: Optional[str] = None
    is_public: Optional[bool] = None
    is_favorite: Optional[bool] = None


class RoutineResponse(RoutineBase):
    """Schema for routine response"""
    id: int
    user_id: int
    times_completed: int
    created_at: datetime
    updated_at: datetime
    exercises: list[RoutineExerciseResponse] = []

    class Config:
        orm_mode = True


# Nutrition schemas
class NutritionEntryBase(BaseModel):
    """Base nutrition entry schema"""
    date: date  # Date object
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    food_name: str = Field(..., max_length=255)
    brand: Optional[str] = None
    serving_size: Optional[float] = None
    serving_unit: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    sodium: Optional[float] = None
    notes: Optional[str] = None


class NutritionEntryCreate(NutritionEntryBase):
    """Schema for nutrition entry creation"""
    pass


class NutritionEntryUpdate(BaseModel):
    """Schema for nutrition entry update"""
    date: Optional[date] = None
    meal_type: Optional[str] = Field(None, pattern="^(breakfast|lunch|dinner|snack)$")
    food_name: Optional[str] = Field(None, max_length=255)
    brand: Optional[str] = None
    serving_size: Optional[float] = None
    serving_unit: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    sodium: Optional[float] = None
    notes: Optional[str] = None


class NutritionEntryResponse(NutritionEntryBase):
    """Schema for nutrition entry response"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class NutritionSummaryResponse(BaseModel):
    """Schema for nutrition summary response"""
    date: date
    total_calories: float
    total_protein: float
    total_carbohydrates: float
    total_fat: float
    total_fiber: float
    total_sugar: float
    total_sodium: float
    meals_summary: dict
    entries_count: int


# Progress schemas
class ProgressEntryBase(BaseModel):
    """Base progress entry schema"""
    date: str  # ISO date string
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    muscle_mass: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    bicep_left: Optional[float] = None
    bicep_right: Optional[float] = None
    thigh_left: Optional[float] = None
    thigh_right: Optional[float] = None
    front_photo_url: Optional[str] = None
    side_photo_url: Optional[str] = None
    back_photo_url: Optional[str] = None
    max_bench_press: Optional[float] = None
    max_squat: Optional[float] = None
    max_deadlift: Optional[float] = None
    max_pullups: Optional[int] = None
    max_pushups: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    mile_time_seconds: Optional[int] = None
    flexibility_score: Optional[float] = None
    notes: Optional[str] = None


class ProgressEntryCreate(ProgressEntryBase):
    """Schema for progress entry creation"""
    pass


class ProgressEntryResponse(ProgressEntryBase):
    """Schema for progress entry response"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Workout session schemas
class WorkoutSessionBase(BaseModel):
    """Base workout session schema"""
    routine_id: Optional[int] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class WorkoutSessionCreate(WorkoutSessionBase):
    """Schema for workout session creation"""
    pass


class WorkoutSessionResponse(WorkoutSessionBase):
    """Schema for workout session response"""
    id: int
    user_id: int
    created_at: datetime
    routine: Optional[RoutineResponse] = None

    class Config:
        orm_mode = True


# Progress tracking additional schemas
class ProgressEntryUpdate(BaseModel):
    """Schema for progress entry updates"""
    date: Optional[str] = None
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    muscle_mass: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    bicep_left: Optional[float] = None
    bicep_right: Optional[float] = None
    thigh_left: Optional[float] = None
    thigh_right: Optional[float] = None
    front_photo_url: Optional[str] = None
    side_photo_url: Optional[str] = None
    back_photo_url: Optional[str] = None
    max_bench_press: Optional[float] = None
    max_squat: Optional[float] = None
    max_deadlift: Optional[float] = None
    max_pullups: Optional[int] = None
    max_pushups: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    mile_time_seconds: Optional[int] = None
    flexibility_score: Optional[float] = None
    notes: Optional[str] = None


class ProgressAnalytics(BaseModel):
    """Schema for progress analytics"""
    metric: str
    current_value: Optional[float]
    previous_value: Optional[float]
    change: Optional[float]
    change_percentage: Optional[float]
    trend: str  # increasing, decreasing, stable
    period_days: int


class ProgressReport(BaseModel):
    """Schema for comprehensive progress reports"""
    start_date: str
    end_date: str
    weight_analytics: Optional[ProgressAnalytics]
    body_fat_analytics: Optional[ProgressAnalytics]
    muscle_mass_analytics: Optional[ProgressAnalytics]
    strength_analytics: Dict[str, ProgressAnalytics]
    measurements_analytics: Dict[str, ProgressAnalytics]
    total_entries: int
    consistency_score: float  # 0-100


# Goal schemas
class GoalBase(BaseModel):
    """Base goal schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., pattern="^(weight_loss|muscle_gain|strength|endurance|nutrition|other)$")
    target_value: Optional[float] = None
    unit: Optional[str] = None
    target_date: Optional[str] = None  # ISO date string
    priority: Optional[str] = Field("medium", pattern="^(low|medium|high)$")
    is_public: Optional[bool] = False


class GoalCreate(GoalBase):
    """Schema for goal creation"""
    pass


class GoalUpdate(BaseModel):
    """Schema for goal updates"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = None
    target_date: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|paused|cancelled)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    is_public: Optional[bool] = None


class GoalResponse(GoalBase):
    """Schema for goal response"""
    id: int
    user_id: int
    current_value: float
    status: str
    progress_percentage: Optional[float] = None
    days_remaining: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# Notification schemas
class NotificationBase(BaseModel):
    """Base notification schema"""
    title: str = Field(..., min_length=1, max_length=255)
    body: str = Field(..., min_length=1)
    notification_type: str = Field(..., pattern="^(workout_reminder|goal_milestone|progress_update|achievement|custom)$")
    category: Optional[str] = Field(None, pattern="^(exercise|nutrition|progress|social|system)$")
    data: Optional[Dict] = None
    scheduled_for: Optional[datetime] = None


class NotificationCreate(NotificationBase):
    """Schema for notification creation"""
    pass


class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    id: int
    user_id: int
    is_read: bool
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True


class NotificationSettingsBase(BaseModel):
    """Base notification settings schema"""
    workout_reminders: Optional[bool] = True
    goal_milestones: Optional[bool] = True
    progress_updates: Optional[bool] = True
    achievements: Optional[bool] = True
    social_interactions: Optional[bool] = True
    reminder_time_morning: Optional[str] = Field(None, pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    reminder_time_evening: Optional[str] = Field(None, pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    quiet_hours_start: Optional[str] = Field(None, pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    quiet_hours_end: Optional[str] = Field(None, pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")


class NotificationSettingsCreate(NotificationSettingsBase):
    """Schema for notification settings creation"""
    fcm_token: Optional[str] = None
    apns_token: Optional[str] = None


class NotificationSettingsUpdate(NotificationSettingsBase):
    """Schema for notification settings updates"""
    fcm_token: Optional[str] = None
    apns_token: Optional[str] = None


class NotificationSettingsResponse(NotificationSettingsBase):
    """Schema for notification settings response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# Achievement schemas
class AchievementBase(BaseModel):
    """Base achievement schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., pattern="^(exercise|nutrition|consistency|milestones|special)$")
    icon_url: Optional[str] = None
    badge_color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    points: Optional[int] = Field(0, ge=0)


class AchievementResponse(AchievementBase):
    """Schema for achievement response"""
    id: int
    criteria: Optional[Dict] = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserAchievementResponse(BaseModel):
    """Schema for user achievement response"""
    id: int
    user_id: int
    achievement: AchievementResponse
    earned_at: datetime
    progress_value: Optional[float]

    class Config:
        orm_mode = True


# Daily Motivation schemas
class DailyQuoteBase(BaseModel):
    """Base daily quote schema"""
    quote: str = Field(..., min_length=10, max_length=1000)
    author: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, pattern="^(fitness|motivation|success|health|mindset)$")
    language: Optional[str] = Field("es", pattern="^(es|en)$")
    tags: Optional[List[str]] = None


class DailyQuoteResponse(DailyQuoteBase):
    """Schema for daily quote response"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class DailyChallengeBase(BaseModel):
    """Base daily challenge schema"""
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10)
    difficulty_level: str = Field(..., pattern="^(easy|medium|hard)$")
    category: str = Field(..., pattern="^(cardio|strength|flexibility|mindfulness|nutrition)$")
    points_reward: Optional[int] = Field(10, ge=1, le=100)
    estimated_duration: Optional[int] = Field(None, ge=1, le=180)  # minutes
    instructions: Optional[List[str]] = None
    requirements: Optional[List[str]] = None


class DailyChallengeCreate(DailyChallengeBase):
    """Schema for daily challenge creation"""
    pass


class DailyChallengeResponse(DailyChallengeBase):
    """Schema for daily challenge response"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserDailyChallengeLogBase(BaseModel):
    """Base user daily challenge log schema"""
    challenge_id: int
    date: str  # ISO date string
    status: Optional[str] = Field("started", pattern="^(started|completed|skipped|failed)$")
    completion_time: Optional[int] = Field(None, ge=1, le=300)  # minutes
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class UserDailyChallengeLogCreate(UserDailyChallengeLogBase):
    """Schema for user daily challenge log creation"""
    pass


class UserDailyChallengeLogUpdate(BaseModel):
    """Schema for user daily challenge log updates"""
    status: Optional[str] = Field(None, pattern="^(started|completed|skipped|failed)$")
    completion_time: Optional[int] = Field(None, ge=1, le=300)
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class UserDailyChallengeLogResponse(UserDailyChallengeLogBase):
    """Schema for user daily challenge log response"""
    id: int
    user_id: int
    points_earned: int
    completed_at: Optional[datetime]
    created_at: datetime
    challenge: DailyChallengeResponse

    class Config:
        orm_mode = True


class UserStreakBase(BaseModel):
    """Base user streak schema"""
    streak_type: str = Field(..., pattern="^(workout|challenge|login|progress_update)$")
    current_count: Optional[int] = 0
    last_activity_date: Optional[str] = None  # ISO date string


class UserStreakResponse(UserStreakBase):
    """Schema for user streak response"""
    id: int
    user_id: int
    longest_streak: int
    started_at: Optional[str]
    streak_broken_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class MotivationRewardBase(BaseModel):
    """Base motivation reward schema"""
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    reward_type: str = Field(..., pattern="^(streak_milestone|challenge_master|consistency_king|points_milestone)$")
    requirement_value: int = Field(..., ge=1)
    requirement_type: str = Field(..., pattern="^(streak_days|total_points|challenges_completed|workouts_completed)$")
    badge_icon: Optional[str] = None
    badge_color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    points_value: Optional[int] = Field(0, ge=0)


class MotivationRewardResponse(MotivationRewardBase):
    """Schema for motivation reward response"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserMotivationRewardResponse(BaseModel):
    """Schema for user motivation reward response"""
    id: int
    user_id: int
    earned_at: datetime
    achievement_value: Optional[int]
    reward: MotivationRewardResponse

    class Config:
        orm_mode = True


class UserMotivationStatsBase(BaseModel):
    """Base user motivation stats schema"""
    date: str  # ISO date string
    daily_quote_viewed: Optional[bool] = False
    daily_challenge_accepted: Optional[bool] = False
    daily_challenge_completed: Optional[bool] = False
    workouts_completed: Optional[int] = 0
    progress_logged: Optional[bool] = False
    daily_points_earned: Optional[int] = 0
    app_opens: Optional[int] = 0
    time_spent_minutes: Optional[int] = 0


class UserMotivationStatsCreate(UserMotivationStatsBase):
    """Schema for user motivation stats creation"""
    pass


class UserMotivationStatsUpdate(BaseModel):
    """Schema for user motivation stats updates"""
    daily_quote_viewed: Optional[bool] = None
    daily_challenge_accepted: Optional[bool] = None
    daily_challenge_completed: Optional[bool] = None
    workouts_completed: Optional[int] = None
    progress_logged: Optional[bool] = None
    daily_points_earned: Optional[int] = None
    app_opens: Optional[int] = None
    time_spent_minutes: Optional[int] = None


class UserMotivationStatsResponse(UserMotivationStatsBase):
    """Schema for user motivation stats response"""
    id: int
    user_id: int
    motivation_score: float
    achievements_unlocked: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class MotivationLevelResponse(BaseModel):
    """Schema for motivation level response"""
    id: int
    level_number: int
    name: str
    description: Optional[str]
    min_points: int
    max_points: Optional[int]
    level_icon: Optional[str]
    level_color: Optional[str]
    perks: Optional[List[str]]
    created_at: datetime

    class Config:
        orm_mode = True


class DailyMotivationSummary(BaseModel):
    """Schema for daily motivation summary"""
    date: str
    daily_quote: DailyQuoteResponse
    suggested_challenge: DailyChallengeResponse
    current_streaks: List[UserStreakResponse]
    motivation_stats: UserMotivationStatsResponse
    current_level: MotivationLevelResponse
    points_to_next_level: int
    recent_rewards: List[UserMotivationRewardResponse]


class MotivationDashboard(BaseModel):
    """Schema for motivation dashboard"""
    user_level: MotivationLevelResponse
    total_points: int
    active_streaks: List[UserStreakResponse]
    recent_challenges: List[UserDailyChallengeLogResponse]
    earned_rewards: List[UserMotivationRewardResponse]
    weekly_stats: List[UserMotivationStatsResponse]
    motivation_trend: str  # increasing, stable, decreasing
    consistency_score: float  # 0-100