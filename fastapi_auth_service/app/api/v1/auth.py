from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...schemas.user_schema import UserLogin, Token, UserCreateBySuperAdmin, UserResponse, PasswordChange
from ...core.oauth2 import get_current_active_user, require_super_admin, require_client_admin
from ...models.user import User, UserRole
from ...services.auth_service import auth_service

router = APIRouter()


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login endpoint for all users"""
    return auth_service.authenticate_and_create_token(db, user_credentials)


@router.post("/create-client-admin", response_model=UserResponse)
def create_client_admin(
    user_data: UserCreateBySuperAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Create Client Admin account (Super Admin only)"""
    return auth_service.create_client_admin_by_super_admin(db, user_data)


@router.post("/create-organizer", response_model=UserResponse)
def create_organizer(
    user_data: UserCreateBySuperAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_client_admin)
):
    """Create Organizer account (Client Admin or Super Admin only)"""
    # Ensure only Client Admin or Organizer roles can be created
    if user_data.role not in [UserRole.CLIENT_ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only create Client Admin or Organizer accounts"
        )
    
    # If current user is Client Admin, they can only create Organizers
    if current_user.role == UserRole.CLIENT_ADMIN and user_data.role == UserRole.CLIENT_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client Admins can only create Organizer accounts"
        )
    
    # For organizers created by Client Admin, we need to set client_admin_id
    if current_user.role == UserRole.CLIENT_ADMIN and user_data.role == UserRole.ORGANIZER:
        return auth_service.create_organizer_by_client_admin(db, user_data, current_user.id)
    
    return auth_service.create_user_by_super_admin(db, user_data)


@router.get("/users", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Get all users (Super Admin only)"""
    return auth_service.get_all_users(db, skip, limit)


@router.get("/users/client-admins", response_model=List[UserResponse])
def get_client_admins(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Get all Client Admin users (Super Admin only)"""
    return auth_service.get_users_by_role(db, UserRole.CLIENT_ADMIN, skip, limit)


@router.get("/users/organizers", response_model=List[UserResponse])
def get_organizers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_client_admin)
):
    """Get organizers (Client Admin or Super Admin only)"""
    if current_user.role == UserRole.CLIENT_ADMIN:
        # Client Admin can only see their own organizers
        return auth_service.get_organizers_by_client_admin(db, current_user.id, skip, limit)
    else:
        # Super Admin can see all organizers
        return auth_service.get_users_by_role(db, UserRole.ORGANIZER, skip, limit)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Change user password"""
    updated_user = auth_service.change_user_password(db, current_user.id, password_data)
    return {"message": "Password changed successfully"}


@router.post("/users/{user_id}/verify")
def verify_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Verify user account (Super Admin only)"""
    updated_user = auth_service.verify_user_account(db, user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User verified successfully"}


@router.post("/users/{user_id}/deactivate")
def deactivate_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Deactivate user account (Super Admin only)"""
    updated_user = auth_service.deactivate_user_account(db, user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated successfully"}


@router.post("/users/{user_id}/activate")
def activate_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Activate user account (Super Admin only)"""
    updated_user = auth_service.activate_user_account(db, user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User activated successfully"}
