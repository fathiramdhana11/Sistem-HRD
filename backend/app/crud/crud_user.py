# File: backend/app/crud/crud_user.py

from sqlalchemy.orm import Session
from app import models, schemas
from app.schemas.users import UserCreate, UserUpdate 
from app.utils import security

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role_id=user.role_id,
        status='active'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.user.UserUpdate):
    """Mengupdate data user berdasarkan ID."""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None

    # Ambil data dari skema update
    update_data = user_update.dict(exclude_unset=True)

    # Update field di objek user dari database
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user