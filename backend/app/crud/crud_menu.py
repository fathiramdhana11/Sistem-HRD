# File: backend/app/crud/crud_menu.py

from sqlalchemy.orm import Session
# Impor model dan skema secara spesifik untuk menghindari circular import
from app.models.menus import Menu as MenuModel # Ganti 'models.Menu' dengan 'MenuModel' untuk menghindari konflik nama dengan schema.Menu
from app.models.users import User as UserModel # Import User model jika creator/updater perlu di-resolve
# from app.database import Base # Hanya jika Base diperlukan di sini (biasanya tidak untuk CRUD)

from app.schemas.menus import MenuCreate, MenuUpdate # Impor skema MenuCreate dan MenuUpdate
# Jika Anda perlu mengakses skema Menu (untuk respons misalnya, di luar CRUD),
# Anda bisa mengimpornya juga: from app.schemas.menus import Menu 


def get_menu(db: Session, menu_id: int):
    return db.query(MenuModel).filter(MenuModel.menu_id == menu_id).first()

def get_menu_by_route(db: Session, route: str):
    return db.query(MenuModel).filter(MenuModel.route == route).first()

def get_all_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MenuModel).offset(skip).limit(limit).all()

def create_menu(db: Session, menu: MenuCreate, created_by_user_id: int = None):
    db_menu = MenuModel(
        menu_name=menu.menu_name,
        route=menu.route,
        parent_menu_id=menu.parent_menu_id,
        icon=menu.icon,
        order_no=menu.order_no,
        is_active=menu.is_active,
        created_by=created_by_user_id # Mengisi created_by
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menu_id: int, menu_update: MenuUpdate, updated_by_user_id: int = None):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        return None
    
    update_data = menu_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_menu, key, value)
    
    db_menu.updated_by = updated_by_user_id # Mengisi updated_by
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def delete_menu(db: Session, menu_id: int):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        return False
    db.delete(db_menu)
    db.commit()
    return True