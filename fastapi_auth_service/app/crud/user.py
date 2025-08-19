from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.user import User, UserRole
from ..schemas.user_schema import UserCreate, UserCreateBySuperAdmin
from ..core.security import get_password_hash, verify_password
from ..core.config import settings


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users_by_role(db: Session, role: UserRole, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        organization_name=user.organization_name,
        organization_description=user.organization_description,
        client_admin_id=user.client_admin_id,
        organizer_details=user.organizer_details
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_by_super_admin(db: Session, user: UserCreateBySuperAdmin):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        organization_name=user.organization_name,
        organization_description=user.organization_description,
        is_verified=True  # Client Admins created by Super Admin are automatically verified
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_organizer_by_client_admin(db: Session, user: UserCreateBySuperAdmin, client_admin_id: int):
    """Create Organizer account by Client Admin with client_admin_id"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        organization_name=user.organization_name,
        organization_description=user.organization_description,
        client_admin_id=client_admin_id,  # Set the client_admin_id
        is_verified=True  # Organizers created by Client Admin are automatically verified
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def update_user(db: Session, user_id: int, **kwargs):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def get_organizers_by_client_admin(db: Session, client_admin_id: int, skip: int = 0, limit: int = 100):
    return db.query(User).filter(
        and_(
            User.role == UserRole.ORGANIZER,
            User.client_admin_id == client_admin_id
        )
    ).offset(skip).limit(limit).all()


def create_super_admin_if_not_exists(db: Session):
    """Create Super Admin account if it doesn't exist"""
    existing_super_admin = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
    
    if not existing_super_admin:
        hashed_password = get_password_hash(settings.SUPER_ADMIN_PASSWORD)
        super_admin = User(
            username=settings.SUPER_ADMIN_USERNAME,
            email=settings.SUPER_ADMIN_EMAIL,
            hashed_password=hashed_password,
            role=UserRole.SUPER_ADMIN,
            is_active=True,
            is_verified=True
        )
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)
        return super_admin
    
    return existing_super_admin


def change_password(db: Session, user_id: int, new_password: str):
    """Change user password"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_user(db: Session, user_id: int):
    """Mark user as verified"""
    return update_user(db, user_id, is_verified=True)


def deactivate_user(db: Session, user_id: int):
    """Deactivate user account"""
    return update_user(db, user_id, is_active=False)


def activate_user(db: Session, user_id: int):
    """Activate user account"""
    return update_user(db, user_id, is_active=True)
