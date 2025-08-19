#!/usr/bin/env python3
"""
Database initialization script for FastAPI Auth Service
This script creates the database tables and initializes the Super Admin account.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models.user import User
from app.services.auth_service import auth_service
from app.core.config import settings


def init_database():
    """Initialize database tables and Super Admin account"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    print("Initializing Super Admin account...")
    db = SessionLocal()
    try:
        super_admin = auth_service.initialize_super_admin(db)
        print(f"Super Admin account created/verified:")
        print(f"  Username: {super_admin.username}")
        print(f"  Email: {super_admin.email}")
        print(f"  Role: {super_admin.role}")
        print(f"  ID: {super_admin.id}")
        print("\nDefault Super Admin credentials:")
        print(f"  Username: {settings.SUPER_ADMIN_USERNAME}")
        print(f"  Password: {settings.SUPER_ADMIN_PASSWORD}")
        print("\n⚠️  IMPORTANT: Change the Super Admin password after first login!")
        
    except Exception as e:
        print(f"Error initializing Super Admin: {e}")
    finally:
        db.close()
    
    print("\nDatabase initialization completed!")


if __name__ == "__main__":
    init_database()
