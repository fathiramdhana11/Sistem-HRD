# File: backend/app/crud/crud_role_menu_access.py

from sqlalchemy.orm import Session
# Impor model dan skema secara spesifik untuk menghindari circular import
from app.models.role_menu_access import RoleMenuAccess as ModelRoleMenuAccess
from app.models.roles import Role as ModelRole
from app.models.menus import Menu as ModelMenu
from app.models.users import User as UserModel # Untuk created_by/updated_by

from app.schemas.role_menu_access import RoleMenuAccessCreate

def get_role_menu_access_by_ids(db: Session, role_id: int, menu_id: int):
    return db.query(ModelRoleMenuAccess).filter(
        ModelRoleMenuAccess.role_id == role_id,
        ModelRoleMenuAccess.menu_id == menu_id
    ).first()

def get_all_role_menu_access(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelRoleMenuAccess).offset(skip).limit(limit).all()

def create_role_menu_access(db: Session, access: RoleMenuAccessCreate, created_by_user_id: int = None):
    db_access = ModelRoleMenuAccess(
        role_id=access.role_id,
        menu_id=access.menu_id,
        created_by=created_by_user_id
    )
    db.add(db_access)
    db.commit()
    db.refresh(db_access)
    return db_access

def delete_role_menu_access(db: Session, role_id: int, menu_id: int):
    db_access = get_role_menu_access_by_ids(db, role_id, menu_id)
    if not db_access:
        return False
    db.delete(db_access)
    db.commit()
    return True