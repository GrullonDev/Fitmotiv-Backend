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


# ================================
# NEW SCHEMAS FOR FRONTEND COMPATIBILITY
# ================================

# User Profile Schemas
class UserProfileBase(BaseModel):
    """Base schema for user profile"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    timezone: Optional[str] = Field(None, max_length=50)
    
    # Physical
    height: Optional[float] = Field(None, ge=50, le=300)  # cm
    current_weight: Optional[float] = Field(None, ge=20, le=500)  # kg
    target_weight: Optional[float] = Field(None, ge=20, le=500)  # kg
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    body_type: Optional[str] = Field(None, pattern="^(ectomorph|mesomorph|endomorph)$")
    
    # Fitness
    fitness_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    activity_level: Optional[str] = Field(None, pattern="^(sedentary|lightly_active|moderately_active|very_active|extremely_active)$")
    primary_goal: Optional[str] = Field(None, pattern="^(lose_weight|gain_muscle|maintain_weight|improve_endurance|general_fitness)$")
    secondary_goals: Optional[List[str]] = None
    
    # Preferences
    preferred_workout_time: Optional[str] = Field(None, pattern="^(morning|afternoon|evening)$")
    workout_frequency_goal: Optional[int] = Field(None, ge=1, le=14)
    available_equipment: Optional[List[str]] = None
    workout_duration_preference: Optional[int] = Field(None, ge=5, le=300)  # minutes
    
    # Health
    medical_conditions: Optional[List[str]] = None
    injuries_limitations: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    
    # Social
    bio: Optional[str] = Field(None, max_length=1000)
    motivation_level: Optional[int] = Field(5, ge=1, le=10)
    workout_buddy_preference: Optional[bool] = False
    public_profile: Optional[bool] = False
    share_progress: Optional[bool] = True
    
    # Media
    profile_picture_url: Optional[str] = Field(None, max_length=500)
    cover_photo_url: Optional[str] = Field(None, max_length=500)
    
    # Settings
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    marketing_emails: Optional[bool] = False
    data_sharing: Optional[bool] = False
    measurement_unit: Optional[str] = Field("metric", pattern="^(metric|imperial)$")
    language: Optional[str] = Field("es", pattern="^(es|en)$")
    theme: Optional[str] = Field("light", pattern="^(light|dark|auto)$")


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile"""
    pass


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    height: Optional[float] = Field(None, ge=50, le=300)
    current_weight: Optional[float] = Field(None, ge=20, le=500)
    target_weight: Optional[float] = Field(None, ge=20, le=500)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    fitness_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    primary_goal: Optional[str] = Field(None, pattern="^(lose_weight|gain_muscle|maintain_weight|improve_endurance|general_fitness)$")
    bio: Optional[str] = Field(None, max_length=1000)
    profile_picture_url: Optional[str] = Field(None, max_length=500)


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Weight Tracking Schemas
class WeightEntryBase(BaseModel):
    """Base schema for weight entry"""
    date: date
    weight: float = Field(..., ge=20, le=500)  # kg
    body_fat_percentage: Optional[float] = Field(None, ge=0, le=100)
    muscle_mass_percentage: Optional[float] = Field(None, ge=0, le=100)
    water_percentage: Optional[float] = Field(None, ge=0, le=100)
    bone_mass: Optional[float] = Field(None, ge=0, le=50)
    visceral_fat: Optional[float] = Field(None, ge=0, le=100)
    metabolic_age: Optional[int] = Field(None, ge=10, le=120)
    
    # Measurements
    waist: Optional[float] = Field(None, ge=10, le=300)  # cm
    chest: Optional[float] = Field(None, ge=10, le=300)
    hips: Optional[float] = Field(None, ge=10, le=300)
    neck: Optional[float] = Field(None, ge=10, le=100)
    bicep: Optional[float] = Field(None, ge=10, le=100)
    thigh: Optional[float] = Field(None, ge=10, le=200)
    
    notes: Optional[str] = Field(None, max_length=1000)
    mood: Optional[str] = Field(None, pattern="^(great|good|okay|bad|terrible)$")
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    progress_photo_url: Optional[str] = Field(None, max_length=500)
    measurement_method: Optional[str] = Field("scale", pattern="^(scale|tape_measure|body_scan|visual)$")
    measurement_time: Optional[str] = Field(None, pattern="^(morning|evening|after_workout)$")


class WeightEntryCreate(WeightEntryBase):
    """Schema for creating weight entry"""
    pass


class WeightEntryUpdate(BaseModel):
    """Schema for updating weight entry"""
    weight: Optional[float] = Field(None, ge=20, le=500)
    body_fat_percentage: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = Field(None, max_length=1000)
    mood: Optional[str] = Field(None, pattern="^(great|good|okay|bad|terrible)$")
    energy_level: Optional[int] = Field(None, ge=1, le=10)


class WeightEntryResponse(WeightEntryBase):
    """Schema for weight entry response"""
    id: int
    user_id: int
    weight_change: Optional[float]
    weekly_average: Optional[float]
    monthly_average: Optional[float]
    progress_toward_goal: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class WeightProgressSummary(BaseModel):
    """Schema for weight progress summary"""
    current_weight: float
    starting_weight: Optional[float]
    target_weight: Optional[float]
    total_weight_change: Optional[float]
    weight_to_goal: Optional[float]
    progress_percentage: Optional[float]
    recent_entries: List[WeightEntryResponse]
    weekly_average: Optional[float]
    monthly_average: Optional[float]
    trend: str  # increasing, decreasing, stable


# Enhanced Goal Schemas
class GoalBase(BaseModel):
    """Base schema for goals"""
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., pattern="^(weight_loss|muscle_gain|strength|endurance|nutrition|habits)$")
    subcategory: Optional[str] = Field(None, max_length=100)
    target_value: float = Field(..., gt=0)
    starting_value: Optional[float] = Field(None, ge=0)
    unit: str = Field(..., min_length=1, max_length=50)
    target_date: Optional[date] = None
    start_date: Optional[date] = None
    priority: Optional[str] = Field("medium", pattern="^(low|medium|high|critical)$")
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard|extreme)$")
    motivation_reason: Optional[str] = Field(None, max_length=1000)
    reward_for_completion: Optional[str] = Field(None, max_length=255)
    reminder_frequency: Optional[str] = Field(None, pattern="^(daily|weekly|monthly)$")
    goal_image_url: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = False
    tags: Optional[List[str]] = None


class GoalCreate(GoalBase):
    """Schema for creating goal"""
    pass


class GoalUpdate(BaseModel):
    """Schema for updating goal"""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    target_value: Optional[float] = Field(None, gt=0)
    target_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|paused|cancelled)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    motivation_reason: Optional[str] = Field(None, max_length=1000)
    current_value: Optional[float] = Field(None, ge=0)


class GoalResponse(GoalBase):
    """Schema for goal response"""
    id: int
    user_id: int
    current_value: float
    progress_percentage: float
    status: str
    estimated_completion_date: Optional[date]
    last_updated_progress: Optional[date]
    is_smart_goal: bool
    success_probability: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GoalProgressBase(BaseModel):
    """Base schema for goal progress"""
    progress_value: float = Field(..., ge=0)
    notes: Optional[str] = Field(None, max_length=1000)
    mood: Optional[str] = Field(None, pattern="^(motivated|neutral|discouraged)$")
    confidence_level: Optional[int] = Field(None, ge=1, le=10)
    measurement_method: Optional[str] = Field(None, max_length=100)


class GoalProgressCreate(GoalProgressBase):
    """Schema for creating goal progress"""
    pass


class GoalProgressResponse(GoalProgressBase):
    """Schema for goal progress response"""
    id: int
    goal_id: int
    date: date
    progress_change: Optional[float]
    progress_percentage: float
    verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Workout of the Day Schemas
class WorkoutOfTheDayBase(BaseModel):
    """Base schema for workout of the day"""
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10, max_length=2000)
    category: str = Field(..., pattern="^(strength|cardio|flexibility|full_body|hiit)$")
    difficulty_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    estimated_duration: int = Field(..., ge=5, le=180)  # minutes
    calories_estimate: Optional[int] = Field(None, ge=50, le=2000)
    equipment_needed: Optional[List[str]] = None
    space_required: Optional[str] = Field(None, pattern="^(small|medium|large)$")
    target_muscle_groups: Optional[List[str]] = None
    motivation_tip: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)


class WorkoutOfTheDayCreate(WorkoutOfTheDayBase):
    """Schema for creating workout of the day"""
    date: date
    warm_up_exercises: Optional[List[Dict]] = None
    main_exercises: List[Dict] = Field(..., min_items=1)
    cool_down_exercises: Optional[List[Dict]] = None
    form_tips: Optional[List[str]] = None
    modifications: Optional[List[Dict]] = None


class WorkoutOfTheDayResponse(WorkoutOfTheDayBase):
    """Schema for workout of the day response"""
    id: int
    date: date
    warm_up_exercises: Optional[List[Dict]]
    main_exercises: List[Dict]
    cool_down_exercises: Optional[List[Dict]]
    form_tips: Optional[List[str]]
    modifications: Optional[List[Dict]]
    completion_count: int
    average_rating: float
    is_active: bool
    featured: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserWorkoutCompletionBase(BaseModel):
    """Base schema for user workout completion"""
    actual_duration: Optional[int] = Field(None, ge=1, le=300)
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5)
    enjoyment_rating: Optional[int] = Field(None, ge=1, le=5)
    exercises_completed: Optional[List[Dict]] = None
    modifications_used: Optional[List[Dict]] = None
    calories_burned: Optional[int] = Field(None, ge=10, le=2000)
    notes: Optional[str] = Field(None, max_length=1000)
    favorite: Optional[bool] = False
    would_repeat: Optional[bool] = True


class UserWorkoutCompletionCreate(UserWorkoutCompletionBase):
    """Schema for creating workout completion"""
    pass


class UserWorkoutCompletionResponse(UserWorkoutCompletionBase):
    """Schema for workout completion response"""
    id: int
    user_id: int
    workout_id: int
    completed_at: datetime

    class Config:
        from_attributes = True


# Dashboard Schemas
class FitnessDashboard(BaseModel):
    """Main fitness dashboard schema"""
    user_profile: UserProfileResponse
    weight_progress: WeightProgressSummary
    active_goals: List[GoalResponse]
    recent_workouts: List[UserWorkoutCompletionResponse]
    today_workout: Optional[WorkoutOfTheDayResponse]
    motivation_summary: DailyMotivationSummary
    weekly_stats: Dict[str, float]


class ProfileEditRequest(BaseModel):
    """Schema for profile edit requests from frontend"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    height: Optional[float] = None
    current_weight: Optional[float] = None
    target_weight: Optional[float] = None
    fitness_level: Optional[str] = None
    primary_goal: Optional[str] = None
    bio: Optional[str] = None