# File: backend/app/crud/crud_role.py

from sqlalchemy.orm import Session
from app import models, schemas

def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.role_id == role_id).first()

def get_all_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(role_name=role.role_name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Anda bisa menambahkan fungsi update_role dan delete_role di sini juga jika diperlukan