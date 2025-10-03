"""
Authentication router - handles login, register, logout
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.models import User
from app.schemas import (
    UserCreate, UserResponse, LoginRequest, Token, 
    MessageResponse, PasswordChange
)
from app.security import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_active_user, security, verify_password
)
from app.blacklist import add_token_to_blacklist
from app.config import get_settings

# Get settings instance
settings = get_settings()

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        age=user_data.age,
        height=user_data.height,
        weight=user_data.weight,
        fitness_goal=user_data.fitness_goal,
        activity_level=user_data.activity_level,
        bio=user_data.bio
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return access token"""
    
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", response_model=MessageResponse)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_active_user)
):
    """Logout user by blacklisting the current token"""
    
    token = credentials.credentials
    add_token_to_blacklist(token)
    
    return {"message": "Successfully logged out"}


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.get("/verify-token", response_model=UserResponse)
async def verify_token(current_user: User = Depends(get_current_active_user)):
    """Verify if the current token is valid and return user info"""
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: dict, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        from app.security import verify_token, create_refresh_token
        
        # Verify refresh token
        token_info = verify_token(token_data.get("refresh_token"), "refresh")
        
        # Get user
        user = db.query(User).filter(User.username == token_info.username).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        new_access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        new_refresh_token = create_refresh_token(data={"sub": user.username})
        
        # Blacklist old refresh token for security
        add_token_to_blacklist(token_data.get("refresh_token"))
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/forgot-password", response_model=MessageResponse)
@limiter.limit("3/minute")
async def forgot_password(request: Request, email_data: dict, db: Session = Depends(get_db)):
    """Send password reset email"""
    from app.security import create_reset_token, send_password_reset_email
    
    email = email_data.get("email")
    user = db.query(User).filter(User.email == email).first()
    
    # Always return success to prevent email enumeration
    if user:
        reset_token = create_reset_token(user.email)
        send_password_reset_email(user.email, reset_token)
    
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(reset_data: dict, db: Session = Depends(get_db)):
    """Reset password using reset token"""
    try:
        from app.security import verify_token
        
        token = reset_data.get("token")
        new_password = reset_data.get("new_password")
        
        # Verify reset token
        token_info = verify_token(token, "reset")
        
        # Find user by email (stored in token subject)
        user = db.query(User).filter(User.email == token_info.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        # Update password
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        
        return {"message": "Password successfully reset"}
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(verification_data: dict, db: Session = Depends(get_db)):
    """Verify email using verification token"""
    try:
        from app.security import verify_token
        
        token = verification_data.get("token")
        
        # Verify token
        token_info = verify_token(token, "verification")
        
        # Find user by email (stored in token subject)
        user = db.query(User).filter(User.email == token_info.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )
        
        # Mark email as verified
        user.is_verified = True
        db.commit()
        
        return {"message": "Email successfully verified"}
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification(email_data: dict, db: Session = Depends(get_db)):
    """Resend email verification"""
    from app.security import create_verification_token, send_verification_email
    
    email = email_data.get("email")
    user = db.query(User).filter(User.email == email).first()
    
    if user and not user.is_verified:
        verification_token = create_verification_token(user.email)
        send_verification_email(user.email, verification_token)
    
    return {"message": "If the email exists and is unverified, a verification link has been sent"}