"""
Database models for the application
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Basic profile information (keep for backwards compatibility)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)  # in cm
    weight = Column(Float, nullable=True)  # in kg
    gender = Column(String(20), nullable=True)  # M, F, Other
    fitness_goal = Column(String(100), nullable=True)  # lose_weight, gain_muscle, maintain, etc.
    activity_level = Column(String(50), nullable=True)  # sedentary, light, moderate, active, very_active
    bio = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    routines = relationship("Routine", back_populates="user")
    nutrition_entries = relationship("NutritionEntry", back_populates="user")
    progress_entries = relationship("ProgressEntry", back_populates="user")
    weight_entries = relationship("WeightEntry", back_populates="user")
    workout_sessions = relationship("WorkoutSession", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    notification_settings = relationship("NotificationSetting", back_populates="user", uselist=False)
    user_achievements = relationship("UserAchievement", back_populates="user")
    daily_challenge_logs = relationship("UserDailyChallengeLog", back_populates="user")
    streaks = relationship("UserStreak", back_populates="user")
    motivation_rewards = relationship("UserMotivationReward", back_populates="user")
    motivation_stats = relationship("UserMotivationStats", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class UserProfile(Base):
    """Extended user profile model for frontend compatibility"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Personal Information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone_number = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    timezone = Column(String(50), nullable=True)
    
    # Physical Attributes
    height = Column(Float, nullable=True)  # cm
    current_weight = Column(Float, nullable=True)  # kg
    target_weight = Column(Float, nullable=True)  # kg
    gender = Column(String(20), nullable=True)  # male, female, other
    body_type = Column(String(50), nullable=True)  # ectomorph, mesomorph, endomorph
    
    # Fitness Profile
    fitness_level = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    activity_level = Column(String(50), nullable=True)  # sedentary, lightly_active, moderately_active, very_active, extremely_active
    primary_goal = Column(String(100), nullable=True)  # lose_weight, gain_muscle, maintain_weight, improve_endurance, general_fitness
    secondary_goals = Column(JSON, nullable=True)  # ["improve_strength", "increase_flexibility"]
    
    # Preferences
    preferred_workout_time = Column(String(50), nullable=True)  # morning, afternoon, evening
    workout_frequency_goal = Column(Integer, nullable=True)  # times per week
    available_equipment = Column(JSON, nullable=True)  # ["dumbbells", "resistance_bands", "none"]
    workout_duration_preference = Column(Integer, nullable=True)  # minutes
    
    # Medical & Health
    medical_conditions = Column(JSON, nullable=True)  # ["diabetes", "hypertension"]
    injuries_limitations = Column(JSON, nullable=True)  # ["lower_back_pain", "knee_injury"]
    medications = Column(JSON, nullable=True)
    allergies = Column(JSON, nullable=True)
    
    # Social & Motivation
    bio = Column(Text, nullable=True)
    motivation_level = Column(Integer, default=5)  # 1-10 scale
    workout_buddy_preference = Column(Boolean, default=False)
    public_profile = Column(Boolean, default=False)
    share_progress = Column(Boolean, default=True)
    
    # Media
    profile_picture_url = Column(String(500), nullable=True)
    cover_photo_url = Column(String(500), nullable=True)
    
    # Notifications & Privacy
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    marketing_emails = Column(Boolean, default=False)
    data_sharing = Column(Boolean, default=False)
    
    # App Settings
    measurement_unit = Column(String(20), default="metric")  # metric, imperial
    language = Column(String(10), default="es")  # es, en
    theme = Column(String(20), default="light")  # light, dark, auto
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")


class Exercise(Base):
    """Exercise model"""
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), nullable=False)  # strength, cardio, flexibility, balance
    muscle_groups = Column(JSON)  # ["chest", "triceps", "shoulders"]
    equipment_needed = Column(JSON)  # ["dumbbells", "bench"]
    difficulty_level = Column(String(50))  # beginner, intermediate, advanced
    instructions = Column(Text)
    video_url = Column(String(500))
    image_url = Column(String(500))
    is_custom = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    routine_exercises = relationship("RoutineExercise", back_populates="exercise")
    exercise_logs = relationship("ExerciseLog", back_populates="exercise")


class Routine(Base):
    """Routine model"""
    __tablename__ = "routines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    difficulty_level = Column(String(50))  # beginner, intermediate, advanced
    duration_minutes = Column(Integer)  # estimated duration
    category = Column(String(100))  # full_body, upper_body, lower_body, cardio, etc.
    is_public = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    times_completed = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="routines")
    exercises = relationship("RoutineExercise", back_populates="routine")
    workout_sessions = relationship("WorkoutSession", back_populates="routine")


class RoutineExercise(Base):
    """Association table for routines and exercises"""
    __tablename__ = "routine_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    order_in_routine = Column(Integer, nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)  # kg
    duration_seconds = Column(Integer)  # for cardio or timed exercises
    rest_seconds = Column(Integer)
    notes = Column(Text)
    
    # Relationships
    routine = relationship("Routine", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="routine_exercises")


class WorkoutSession(Base):
    """Workout session model"""
    __tablename__ = "workout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    calories_burned = Column(Integer)
    notes = Column(Text)
    rating = Column(Integer)  # 1-5 stars
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="workout_sessions")
    routine = relationship("Routine", back_populates="workout_sessions")
    exercise_logs = relationship("ExerciseLog", back_populates="workout_session")


class ExerciseLog(Base):
    """Exercise log model for tracking individual exercise performance"""
    __tablename__ = "exercise_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets_completed = Column(Integer)
    reps_completed = Column(Integer)
    weight_used = Column(Float)  # kg
    duration_seconds = Column(Integer)
    calories_burned = Column(Integer)
    notes = Column(Text)
    
    # Relationships
    workout_session = relationship("WorkoutSession", back_populates="exercise_logs")
    exercise = relationship("Exercise", back_populates="exercise_logs")


class NutritionEntry(Base):
    """Nutrition entry model"""
    __tablename__ = "nutrition_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    food_name = Column(String(255), nullable=False)
    brand = Column(String(255))
    serving_size = Column(Float)
    serving_unit = Column(String(50))  # grams, cups, pieces, etc.
    
    # Nutritional information per serving
    calories = Column(Float)
    protein = Column(Float)  # grams
    carbohydrates = Column(Float)  # grams
    fat = Column(Float)  # grams
    fiber = Column(Float)  # grams
    sugar = Column(Float)  # grams
    sodium = Column(Float)  # mg
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="nutrition_entries")


class ProgressEntry(Base):
    """Progress tracking model"""
    __tablename__ = "progress_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Body measurements
    weight = Column(Float)  # kg
    body_fat_percentage = Column(Float)
    muscle_mass = Column(Float)  # kg
    
    # Body measurements (cm)
    chest = Column(Float)
    waist = Column(Float)
    hips = Column(Float)
    bicep_left = Column(Float)
    bicep_right = Column(Float)
    thigh_left = Column(Float)
    thigh_right = Column(Float)
    
    # Photos
    front_photo_url = Column(String(500))
    side_photo_url = Column(String(500))
    back_photo_url = Column(String(500))
    
    # Performance metrics
    max_bench_press = Column(Float)  # kg
    max_squat = Column(Float)  # kg
    max_deadlift = Column(Float)  # kg
    max_pullups = Column(Integer)
    max_pushups = Column(Integer)
    
    # Fitness tests
    resting_heart_rate = Column(Integer)  # bpm
    mile_time_seconds = Column(Integer)
    flexibility_score = Column(Float)
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress_entries")


class WeightEntry(Base):
    """Specific model for weight tracking and loss progress"""
    __tablename__ = "weight_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Weight measurements
    weight = Column(Float, nullable=False)  # kg
    body_fat_percentage = Column(Float, nullable=True)
    muscle_mass_percentage = Column(Float, nullable=True)
    water_percentage = Column(Float, nullable=True)
    bone_mass = Column(Float, nullable=True)
    visceral_fat = Column(Float, nullable=True)
    metabolic_age = Column(Integer, nullable=True)
    
    # Body measurements (cm)
    waist = Column(Float, nullable=True)
    chest = Column(Float, nullable=True)
    hips = Column(Float, nullable=True)
    neck = Column(Float, nullable=True)
    bicep = Column(Float, nullable=True)
    thigh = Column(Float, nullable=True)
    
    # Progress tracking
    weight_change = Column(Float, nullable=True)  # vs previous entry
    weekly_average = Column(Float, nullable=True)
    monthly_average = Column(Float, nullable=True)
    progress_toward_goal = Column(Float, nullable=True)  # percentage
    
    # Additional data
    notes = Column(Text, nullable=True)
    mood = Column(String(50), nullable=True)  # great, good, okay, bad, terrible
    energy_level = Column(Integer, nullable=True)  # 1-10 scale
    
    # Photos for progress comparison
    progress_photo_url = Column(String(500), nullable=True)
    
    # Tracking method
    measurement_method = Column(String(50), default="scale")  # scale, tape_measure, body_scan, visual
    measurement_time = Column(String(50), nullable=True)  # morning, evening, after_workout
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="weight_entries")


class WorkoutOfTheDay(Base):
    """Daily workout recommendations"""
    __tablename__ = "workout_of_the_day"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    
    # Workout details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)  # strength, cardio, flexibility, full_body, hiit
    difficulty_level = Column(String(50), nullable=False)  # beginner, intermediate, advanced
    estimated_duration = Column(Integer, nullable=False)  # minutes
    calories_estimate = Column(Integer, nullable=True)
    
    # Workout structure
    warm_up_exercises = Column(JSON, nullable=True)  # List of warm-up exercises
    main_exercises = Column(JSON, nullable=False)  # Main workout exercises with sets/reps
    cool_down_exercises = Column(JSON, nullable=True)  # Cool-down exercises
    
    # Equipment and requirements
    equipment_needed = Column(JSON, nullable=True)  # ["dumbbells", "mat", "none"]
    space_required = Column(String(100), nullable=True)  # small, medium, large
    target_muscle_groups = Column(JSON, nullable=True)  # ["chest", "legs", "core"]
    
    # Motivation and guidance
    motivation_tip = Column(Text, nullable=True)
    form_tips = Column(JSON, nullable=True)  # Tips for proper form
    modifications = Column(JSON, nullable=True)  # Easier/harder variations
    
    # Media
    video_url = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    
    # Engagement
    completion_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserWorkoutCompletion(Base):
    """Track user's completion of workout of the day"""
    __tablename__ = "user_workout_completions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_id = Column(Integer, ForeignKey("workout_of_the_day.id"), nullable=False)
    
    # Completion details
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    actual_duration = Column(Integer, nullable=True)  # actual time taken in minutes
    difficulty_rating = Column(Integer, nullable=True)  # 1-5 user rating
    enjoyment_rating = Column(Integer, nullable=True)  # 1-5 user rating
    
    # Performance tracking
    exercises_completed = Column(JSON, nullable=True)  # Which exercises were completed
    modifications_used = Column(JSON, nullable=True)  # Which modifications were used
    calories_burned = Column(Integer, nullable=True)
    
    # Feedback
    notes = Column(Text, nullable=True)
    favorite = Column(Boolean, default=False)
    would_repeat = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User")
    workout = relationship("WorkoutOfTheDay")


class Goal(Base):
    """Enhanced goal model for fitness objectives"""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Goal definition
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # weight_loss, muscle_gain, strength, endurance, nutrition, habits
    subcategory = Column(String(100), nullable=True)  # specific goal type
    
    # Target and progress
    target_value = Column(Float, nullable=False)  # target weight, body fat %, etc.
    current_value = Column(Float, default=0.0)
    starting_value = Column(Float, nullable=True)  # baseline value
    unit = Column(String(50), nullable=False)  # kg, %, reps, minutes, etc.
    
    # Timeline
    target_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    estimated_completion_date = Column(Date, nullable=True)
    
    # Status and priority
    status = Column(String(50), default="active")  # active, completed, paused, cancelled, overdue
    priority = Column(String(50), default="medium")  # low, medium, high, critical
    difficulty = Column(String(50), nullable=True)  # easy, medium, hard, extreme
    
    # Progress tracking
    progress_percentage = Column(Float, default=0.0)
    milestones = Column(JSON, nullable=True)  # Intermediate milestones
    milestones_achieved = Column(JSON, nullable=True)  # Completed milestones
    last_updated_progress = Column(Date, nullable=True)
    
    # Motivation and accountability
    motivation_reason = Column(Text, nullable=True)  # Why this goal matters
    reward_for_completion = Column(String(255), nullable=True)  # Self-reward
    accountability_partner = Column(String(255), nullable=True)
    reminder_frequency = Column(String(50), nullable=True)  # daily, weekly, monthly
    
    # Visual tracking
    goal_image_url = Column(String(500), nullable=True)  # Motivational image
    progress_chart_data = Column(JSON, nullable=True)  # Historical progress data
    
    # Social and sharing
    is_public = Column(Boolean, default=False)
    allow_support = Column(Boolean, default=True)  # Allow others to cheer/support
    tags = Column(JSON, nullable=True)  # ["summer_body", "marathon_training"]
    
    # Smart goal features
    is_smart_goal = Column(Boolean, default=False)  # Specific, Measurable, Achievable, Relevant, Time-bound
    specific_criteria = Column(JSON, nullable=True)  # Detailed success criteria
    measurement_method = Column(String(100), nullable=True)  # How progress is measured
    
    # Analytics
    average_weekly_progress = Column(Float, default=0.0)
    predicted_completion_date = Column(Date, nullable=True)
    success_probability = Column(Float, default=0.0)  # AI prediction 0-1
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="goals")


class GoalProgress(Base):
    """Track daily/weekly progress towards goals"""
    __tablename__ = "goal_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Progress data
    progress_value = Column(Float, nullable=False)
    progress_change = Column(Float, nullable=True)  # change from previous entry
    progress_percentage = Column(Float, nullable=False)
    
    # Context
    notes = Column(Text, nullable=True)
    mood = Column(String(50), nullable=True)  # motivated, neutral, discouraged
    confidence_level = Column(Integer, nullable=True)  # 1-10 scale
    
    # Tracking method
    measurement_method = Column(String(100), nullable=True)
    verified = Column(Boolean, default=False)  # If progress was verified/validated
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    goal = relationship("Goal")


class Notification(Base):
    """Notification model for push notifications"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    notification_type = Column(String(100), nullable=False)  # workout_reminder, goal_milestone, progress_update, achievement
    category = Column(String(100))  # exercise, nutrition, progress, social
    data = Column(JSON)  # Additional data for the notification
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    scheduled_for = Column(DateTime(timezone=True))  # When to send the notification
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")


class NotificationSetting(Base):
    """User notification preferences"""
    __tablename__ = "notification_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Push notification settings
    workout_reminders = Column(Boolean, default=True)
    goal_milestones = Column(Boolean, default=True)
    progress_updates = Column(Boolean, default=True)
    achievements = Column(Boolean, default=True)
    social_interactions = Column(Boolean, default=True)
    
    # Timing preferences
    reminder_time_morning = Column(String(5))  # HH:MM format
    reminder_time_evening = Column(String(5))  # HH:MM format
    quiet_hours_start = Column(String(5))  # HH:MM format
    quiet_hours_end = Column(String(5))  # HH:MM format
    
    # Device tokens for push notifications
    fcm_token = Column(String(500))  # Firebase Cloud Messaging token
    apns_token = Column(String(500))  # Apple Push Notification Service token
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notification_settings")


class Achievement(Base):
    """Achievement model for gamification"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    category = Column(String(100), nullable=False)  # exercise, nutrition, consistency, milestones
    icon_url = Column(String(500))
    badge_color = Column(String(20))  # hex color code
    points = Column(Integer, default=0)  # gamification points
    criteria = Column(JSON)  # Criteria to unlock the achievement
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserAchievement(Base):
    """User earned achievements"""
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    progress_value = Column(Float)  # Value that triggered the achievement
    
    # Relationships
    user = relationship("User", back_populates="user_achievements")
    achievement = relationship("Achievement")
    
    # Unique constraint to prevent duplicate achievements
    __table_args__ = (
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('achievement_id', Integer, ForeignKey('achievements.id')),
        {'extend_existing': True}
    )


class DailyQuote(Base):
    """Daily motivational quotes"""
    __tablename__ = "daily_quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    quote = Column(Text, nullable=False)
    author = Column(String(255))
    category = Column(String(100))  # fitness, motivation, success, health, mindset
    language = Column(String(10), default="es")  # es, en
    is_active = Column(Boolean, default=True)
    tags = Column(JSON)  # ["workout", "strength", "determination"]
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DailyChallenge(Base):
    """Daily fitness challenges"""
    __tablename__ = "daily_challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    difficulty_level = Column(String(50), nullable=False)  # easy, medium, hard
    category = Column(String(100), nullable=False)  # cardio, strength, flexibility, mindfulness, nutrition
    points_reward = Column(Integer, default=10)
    estimated_duration = Column(Integer)  # minutes
    instructions = Column(JSON)  # Step-by-step instructions
    requirements = Column(JSON)  # Equipment or prerequisites needed
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserDailyChallengeLog(Base):
    """Track user's daily challenge participation"""
    __tablename__ = "user_daily_challenge_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("daily_challenges.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(50), default="started")  # started, completed, skipped, failed
    completion_time = Column(Integer)  # actual time taken in minutes
    difficulty_rating = Column(Integer)  # 1-5 user rating
    notes = Column(Text)
    points_earned = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="daily_challenge_logs")
    challenge = relationship("DailyChallenge")


class UserStreak(Base):
    """Track user motivation streaks"""
    __tablename__ = "user_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    streak_type = Column(String(100), nullable=False)  # workout, challenge, login, progress_update
    current_count = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(Date)
    started_at = Column(Date)
    streak_broken_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="streaks")


class MotivationReward(Base):
    """Motivation rewards and milestones"""
    __tablename__ = "motivation_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    reward_type = Column(String(100), nullable=False)  # streak_milestone, challenge_master, consistency_king
    requirement_value = Column(Integer, nullable=False)  # days, points, challenges completed
    requirement_type = Column(String(100), nullable=False)  # streak_days, total_points, challenges_completed
    badge_icon = Column(String(500))  # URL to badge icon
    badge_color = Column(String(20))  # hex color
    points_value = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserMotivationReward(Base):
    """User earned motivation rewards"""
    __tablename__ = "user_motivation_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_id = Column(Integer, ForeignKey("motivation_rewards.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    achievement_value = Column(Integer)  # The value that triggered the reward
    
    # Relationships
    user = relationship("User", back_populates="motivation_rewards")
    reward = relationship("MotivationReward")


class UserMotivationStats(Base):
    """Daily motivation statistics for users"""
    __tablename__ = "user_motivation_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Daily activity tracking
    daily_quote_viewed = Column(Boolean, default=False)
    daily_challenge_accepted = Column(Boolean, default=False)
    daily_challenge_completed = Column(Boolean, default=False)
    workouts_completed = Column(Integer, default=0)
    progress_logged = Column(Boolean, default=False)
    
    # Points and scores
    daily_points_earned = Column(Integer, default=0)
    motivation_score = Column(Float, default=0.0)  # 0-100 calculated score
    
    # Engagement metrics
    app_opens = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    achievements_unlocked = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="motivation_stats")
    
    # Unique constraint for one stats entry per user per day
    __table_args__ = (
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('date', Date),
        {'extend_existing': True}
    )


class MotivationLevel(Base):
    """Motivation level system"""
    __tablename__ = "motivation_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    level_number = Column(Integer, nullable=False, unique=True)
    name = Column(String(255), nullable=False)  # Beginner, Motivated, Dedicated, Champion, Legend
    description = Column(Text)
    min_points = Column(Integer, nullable=False)
    max_points = Column(Integer)
    level_icon = Column(String(500))  # URL to level icon
    level_color = Column(String(20))  # hex color
    perks = Column(JSON)  # Special perks for this level
    created_at = Column(DateTime(timezone=True), server_default=func.now())