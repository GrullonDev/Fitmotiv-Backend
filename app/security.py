"""
Security utilities for JWT tokens, password hashing, and authentication
"""
from datetime import datetime, timedelta
from typing import Optional, Union
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import User
from app.schemas import TokenData
from app.blacklist import is_token_blacklisted

# Get settings instance
settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_reset_token(email: str) -> str:
    """Create password reset token"""
    expire = datetime.utcnow() + timedelta(hours=1)  # Reset tokens expire in 1 hour
    to_encode = {"sub": email, "exp": expire, "type": "reset"}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_verification_token(email: str) -> str:
    """Create email verification token"""
    expire = datetime.utcnow() + timedelta(days=7)  # Verification tokens expire in 7 days
    to_encode = {"sub": email, "exp": expire, "type": "verification"}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str = None) -> TokenData:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        typ: str = payload.get("type")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
            
        if token_type and typ != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
            
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    """Authenticate a user with username/email and password"""
    # Try to find user by username or email
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    token = credentials.credentials
    
    # Check if token is blacklisted
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated"
        )
    
    # Verify token (access tokens only)
    token_data = verify_token(token, "access")
    
    # Get user from database
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def send_email(to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.email_from
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(settings.email_host, settings.email_port)
        server.starttls()  # Enable TLS encryption
        server.login(settings.email_host_user, settings.email_host_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(settings.email_from, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_password_reset_email(email: str, reset_token: str) -> bool:
    """Send password reset email"""
    reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"
    
    subject = "Reset Your Password - FitMotiv"
    body = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>You have requested to reset your password for your FitMotiv account.</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
        <p>This link will expire in 1 hour.</p>
        <p>If you didn't request this password reset, please ignore this email.</p>
        <br>
        <p>Best regards,<br>The FitMotiv Team</p>
    </body>
    </html>
    """
    
    return send_email(email, subject, body, is_html=True)


def send_verification_email(email: str, verification_token: str) -> bool:
    """Send email verification email"""
    verification_url = f"{settings.frontend_url}/verify-email?token={verification_token}"
    
    subject = "Verify Your Email - FitMotiv"
    body = f"""
    <html>
    <body>
        <h2>Welcome to FitMotiv!</h2>
        <p>Thank you for registering with FitMotiv. Please verify your email address to complete your registration.</p>
        <p>Click the link below to verify your email:</p>
        <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
        <p>This link will expire in 7 days.</p>
        <p>If you didn't create this account, please ignore this email.</p>
        <br>
        <p>Best regards,<br>The FitMotiv Team</p>
    </body>
    </html>
    """
    
    return send_email(email, subject, body, is_html=True)