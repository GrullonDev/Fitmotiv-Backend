from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    # Configuración de la aplicación
    app_name: str = "FitMotiv API"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Configuración de la base de datos
    database_url: str = "sqlite:///./fitmotiv.db"
    
    # Configuración JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Configuración de Email
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_host_user: str = ""
    email_host_password: str = ""
    email_from: str = ""
    
    # AWS SES (alternativa)
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    
    # SendGrid (alternativa)
    sendgrid_api_key: str = ""
    
    # Frontend URL para verificación de email
    frontend_url: str = "http://localhost:3000"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

@lru_cache()
def get_settings():
    return Settings()
