from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..crud.user import (
    authenticate_user, 
    create_user_by_super_admin, 
    create_organizer_by_client_admin,
    get_user_by_username,
    get_users_by_role,
    get_all_users,
    get_organizers_by_client_admin,
    create_super_admin_if_not_exists,
    change_password,
    verify_user,
    deactivate_user,
    activate_user
)
from ..models.user import User, UserRole
from ..schemas.user_schema import UserLogin, UserCreateBySuperAdmin, Token, PasswordChange
from ..core.security import create_access_token
from ..core.config import settings
from .email_service import email_service


class AuthService:
    
    @staticmethod
    def authenticate_and_create_token(db: Session, user_credentials: UserLogin):
        """Authenticate user and create access token"""
        user = authenticate_user(db, user_credentials.username, user_credentials.password)
        
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
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role.value},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user
        )
    
    @staticmethod
    def create_client_admin_by_super_admin(db: Session, user_data: UserCreateBySuperAdmin):
        """Create Client Admin account by Super Admin and send credentials via email"""
        
        # Check if username already exists
        existing_user = get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if user_data.email:
            from ..crud.user import get_user_by_email
            existing_email = get_user_by_email(db, user_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create the user
        db_user = create_user_by_super_admin(db, user_data)
        
        # Send credentials via email
        try:
            email_service.send_client_admin_credentials(
                email=user_data.email,
                username=user_data.username,
                password=user_data.password,
                user_id=db_user.id
            )
        except Exception as e:
            # Log the error but don't fail the user creation
            print(f"Failed to send email to {user_data.email}: {str(e)}")
            # You might want to add this to a retry queue in production
        
        return db_user
    
    @staticmethod
    def create_user_by_super_admin(db: Session, user_data: UserCreateBySuperAdmin):
        """Create user account by Super Admin or Client Admin"""
        
        # Check if username already exists
        existing_user = get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if user_data.email:
            from ..crud.user import get_user_by_email
            existing_email = get_user_by_email(db, user_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create the user
        db_user = create_user_by_super_admin(db, user_data)
        
        # Send credentials via email for Client Admins and Organizers
        if user_data.role == UserRole.CLIENT_ADMIN:
            try:
                email_service.send_client_admin_credentials(
                    email=user_data.email,
                    username=user_data.username,
                    password=user_data.password,
                    user_id=db_user.id
                )
            except Exception as e:
                # Log the error but don't fail the user creation
                print(f"Failed to send email to {user_data.email}: {str(e)}")
                # You might want to add this to a retry queue in production
        elif user_data.role == UserRole.ORGANIZER:
            try:
                email_service.send_organizer_credentials(
                    email=user_data.email,
                    username=user_data.username,
                    password=user_data.password,
                    user_id=db_user.id,
                    client_admin_name="Super Administrator"
                )
            except Exception as e:
                # Log the error but don't fail the user creation
                print(f"Failed to send email to {user_data.email}: {str(e)}")
                # You might want to add this to a retry queue in production
        
        return db_user
    
    @staticmethod
    def create_organizer_by_client_admin(db: Session, user_data: UserCreateBySuperAdmin, client_admin_id: int):
        """Create Organizer account by Client Admin with client_admin_id"""
        
        # Check if username already exists
        existing_user = get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if user_data.email:
            from ..crud.user import get_user_by_email
            existing_email = get_user_by_email(db, user_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create the user with client_admin_id
        db_user = create_organizer_by_client_admin(db, user_data, client_admin_id)
        
        # Send credentials via email to the organizer
        try:
            # Get the client admin's name for the email
            from ..crud.user import get_user_by_id
            client_admin = get_user_by_id(db, client_admin_id)
            client_admin_name = client_admin.username if client_admin else "Client Administrator"
            
            email_service.send_organizer_credentials(
                email=user_data.email,
                username=user_data.username,
                password=user_data.password,
                user_id=db_user.id,
                client_admin_name=client_admin_name
            )
        except Exception as e:
            # Log the error but don't fail the user creation
            print(f"Failed to send email to {user_data.email}: {str(e)}")
            # You might want to add this to a retry queue in production
        
        return db_user
    
    @staticmethod
    def get_users_by_role(db: Session, role: UserRole, skip: int = 0, limit: int = 100):
        """Get users by role"""
        return get_users_by_role(db, role, skip, limit)
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        """Get all users"""
        return get_all_users(db, skip, limit)
    
    @staticmethod
    def get_organizers_by_client_admin(db: Session, client_admin_id: int, skip: int = 0, limit: int = 100):
        """Get organizers managed by a specific Client Admin"""
        return get_organizers_by_client_admin(db, client_admin_id, skip, limit)
    
    @staticmethod
    def initialize_super_admin(db: Session):
        """Initialize Super Admin account if it doesn't exist"""
        return create_super_admin_if_not_exists(db)
    
    @staticmethod
    def change_user_password(db: Session, user_id: int, password_data: PasswordChange):
        """Change user password"""
        from ..crud.user import get_user_by_id
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not authenticate_user(db, user.username, password_data.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        return change_password(db, user_id, password_data.new_password)
    
    @staticmethod
    def verify_user_account(db: Session, user_id: int):
        """Verify user account (Super Admin only)"""
        return verify_user(db, user_id)
    
    @staticmethod
    def deactivate_user_account(db: Session, user_id: int):
        """Deactivate user account (Super Admin only)"""
        return deactivate_user(db, user_id)
    
    @staticmethod
    def activate_user_account(db: Session, user_id: int):
        """Activate user account (Super Admin only)"""
        return activate_user(db, user_id)


auth_service = AuthService()
