"""
Profile router for user profile management
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import shutil
import os

from app.database import get_db
from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("/me", response_model=schemas.UserProfileResponse)
async def get_my_profile(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create a default profile if it doesn't exist
        profile = models.UserProfile(
            user_id=current_user.id,
            first_name=current_user.full_name.split()[0] if current_user.full_name else None,
            last_name=" ".join(current_user.full_name.split()[1:]) if current_user.full_name and len(current_user.full_name.split()) > 1 else None,
            current_weight=current_user.weight,
            height=current_user.height,
            bio=current_user.bio
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile


@router.put("/me", response_model=schemas.UserProfileResponse)
async def update_my_profile(
    profile_update: schemas.UserProfileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create profile if it doesn't exist
        profile_data = profile_update.dict(exclude_unset=True)
        profile_data["user_id"] = current_user.id
        profile = models.UserProfile(**profile_data)
        db.add(profile)
    else:
        # Update existing profile
        update_data = profile_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
    
    # Also update basic user fields for backwards compatibility
    if profile_update.first_name and profile_update.last_name:
        current_user.full_name = f"{profile_update.first_name} {profile_update.last_name}"
    if profile_update.current_weight:
        current_user.weight = profile_update.current_weight
    if profile_update.height:
        current_user.height = profile_update.height
    if profile_update.bio:
        current_user.bio = profile_update.bio
    
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/upload-profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload profile picture"""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/profile_pictures"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"user_{current_user.id}_profile.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update profile with new image URL
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = models.UserProfile(
            user_id=current_user.id,
            profile_picture_url=f"/{file_path}"
        )
        db.add(profile)
    else:
        profile.profile_picture_url = f"/{file_path}"
    
    db.commit()
    
    return {"message": "Profile picture uploaded successfully", "url": f"/{file_path}"}


@router.post("/upload-cover-photo")
async def upload_cover_photo(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload cover photo"""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/cover_photos"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"user_{current_user.id}_cover.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update profile with new cover photo URL
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = models.UserProfile(
            user_id=current_user.id,
            cover_photo_url=f"/{file_path}"
        )
        db.add(profile)
    else:
        profile.cover_photo_url = f"/{file_path}"
    
    db.commit()
    
    return {"message": "Cover photo uploaded successfully", "url": f"/{file_path}"}


@router.get("/fitness-preferences")
async def get_fitness_preferences(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's fitness preferences"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        return {}
    
    return {
        "fitness_level": profile.fitness_level,
        "activity_level": profile.activity_level,
        "primary_goal": profile.primary_goal,
        "secondary_goals": profile.secondary_goals,
        "preferred_workout_time": profile.preferred_workout_time,
        "workout_frequency_goal": profile.workout_frequency_goal,
        "available_equipment": profile.available_equipment,
        "workout_duration_preference": profile.workout_duration_preference
    }


@router.put("/fitness-preferences")
async def update_fitness_preferences(
    fitness_level: Optional[str] = None,
    activity_level: Optional[str] = None,
    primary_goal: Optional[str] = None,
    secondary_goals: Optional[list] = None,
    preferred_workout_time: Optional[str] = None,
    workout_frequency_goal: Optional[int] = None,
    available_equipment: Optional[list] = None,
    workout_duration_preference: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's fitness preferences"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create profile if it doesn't exist
        profile = models.UserProfile(
            user_id=current_user.id,
            fitness_level=fitness_level,
            activity_level=activity_level,
            primary_goal=primary_goal,
            secondary_goals=secondary_goals,
            preferred_workout_time=preferred_workout_time,
            workout_frequency_goal=workout_frequency_goal,
            available_equipment=available_equipment,
            workout_duration_preference=workout_duration_preference
        )
        db.add(profile)
    else:
        # Update existing profile
        if fitness_level is not None:
            profile.fitness_level = fitness_level
        if activity_level is not None:
            profile.activity_level = activity_level
        if primary_goal is not None:
            profile.primary_goal = primary_goal
        if secondary_goals is not None:
            profile.secondary_goals = secondary_goals
        if preferred_workout_time is not None:
            profile.preferred_workout_time = preferred_workout_time
        if workout_frequency_goal is not None:
            profile.workout_frequency_goal = workout_frequency_goal
        if available_equipment is not None:
            profile.available_equipment = available_equipment
        if workout_duration_preference is not None:
            profile.workout_duration_preference = workout_duration_preference
    
    db.commit()
    db.refresh(profile)
    
    return {"message": "Fitness preferences updated successfully"}


@router.get("/health-info")
async def get_health_info(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's health information"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        return {}
    
    return {
        "medical_conditions": profile.medical_conditions,
        "injuries_limitations": profile.injuries_limitations,
        "medications": profile.medications,
        "allergies": profile.allergies
    }


@router.put("/health-info")
async def update_health_info(
    medical_conditions: Optional[list] = None,
    injuries_limitations: Optional[list] = None,
    medications: Optional[list] = None,
    allergies: Optional[list] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's health information"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = models.UserProfile(
            user_id=current_user.id,
            medical_conditions=medical_conditions,
            injuries_limitations=injuries_limitations,
            medications=medications,
            allergies=allergies
        )
        db.add(profile)
    else:
        if medical_conditions is not None:
            profile.medical_conditions = medical_conditions
        if injuries_limitations is not None:
            profile.injuries_limitations = injuries_limitations
        if medications is not None:
            profile.medications = medications
        if allergies is not None:
            profile.allergies = allergies
    
    db.commit()
    
    return {"message": "Health information updated successfully"}


@router.get("/settings")
async def get_profile_settings(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's profile settings"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        return {}
    
    return {
        "email_notifications": profile.email_notifications,
        "push_notifications": profile.push_notifications,
        "marketing_emails": profile.marketing_emails,
        "data_sharing": profile.data_sharing,
        "measurement_unit": profile.measurement_unit,
        "language": profile.language,
        "theme": profile.theme,
        "public_profile": profile.public_profile,
        "share_progress": profile.share_progress
    }


@router.put("/settings")
async def update_profile_settings(
    email_notifications: Optional[bool] = None,
    push_notifications: Optional[bool] = None,
    marketing_emails: Optional[bool] = None,
    data_sharing: Optional[bool] = None,
    measurement_unit: Optional[str] = None,
    language: Optional[str] = None,
    theme: Optional[str] = None,
    public_profile: Optional[bool] = None,
    share_progress: Optional[bool] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's profile settings"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = models.UserProfile(
            user_id=current_user.id,
            email_notifications=email_notifications,
            push_notifications=push_notifications,
            marketing_emails=marketing_emails,
            data_sharing=data_sharing,
            measurement_unit=measurement_unit,
            language=language,
            theme=theme,
            public_profile=public_profile,
            share_progress=share_progress
        )
        db.add(profile)
    else:
        if email_notifications is not None:
            profile.email_notifications = email_notifications
        if push_notifications is not None:
            profile.push_notifications = push_notifications
        if marketing_emails is not None:
            profile.marketing_emails = marketing_emails
        if data_sharing is not None:
            profile.data_sharing = data_sharing
        if measurement_unit is not None:
            profile.measurement_unit = measurement_unit
        if language is not None:
            profile.language = language
        if theme is not None:
            profile.theme = theme
        if public_profile is not None:
            profile.public_profile = public_profile
        if share_progress is not None:
            profile.share_progress = share_progress
    
    db.commit()
    
    return {"message": "Profile settings updated successfully"}