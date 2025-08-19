from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:1234@localhost:5432/archery"
    
    # JWT settings
    SECRET_KEY: str = "your-super-secret-key-here-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "venkatesanvenu1769@gmail.com"
    SMTP_PASSWORD: str = "aukc aqad jcqy gurp"
    FROM_EMAIL: str = "venkatesanvenu1769@gmail.com"
    
    # Application settings
    APP_NAME: str = "FastAPI Auth Service"
    LOGIN_URL: str = "http://localhost:8000/login"
    
    # Super Admin default credentials
    SUPER_ADMIN_USERNAME: str = "superadmin"
    SUPER_ADMIN_PASSWORD: str = "superadmin123"
    SUPER_ADMIN_EMAIL: str = "superadmin@archery.com"
    
    class Config:
        env_file = ".env"


settings = Settings()
