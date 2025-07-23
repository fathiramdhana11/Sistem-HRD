# File: backend/app/crud/crud_user_action_log.py

from sqlalchemy.orm import Session
# Impor model dan skema secara spesifik untuk menghindari circular import
from app.models.user_action_logs import UserActionLog as ModelUserActionLog
from app.models.users import User as UserModel # Untuk user_id di log
from app.models.menus import Menu as ModelMenu # Untuk menu_id di log

from app.schemas.user_action_logs import UserActionLogCreate

def get_user_action_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelUserActionLog).offset(skip).limit(limit).all()

def create_user_action_log(db: Session, log: UserActionLogCreate, user_id: int = None, menu_id: int = None):
    db_log = ModelUserActionLog(
        user_id=log.user_id if log.user_id is not None else user_id,
        menu_id=log.menu_id if log.menu_id is not None else menu_id,
        terminal_name=log.terminal_name,
        action=log.action,
        target_id=log.target_id,
        description=log.description,
        ip_address=log.ip_address,
        device_info=log.device_info
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log