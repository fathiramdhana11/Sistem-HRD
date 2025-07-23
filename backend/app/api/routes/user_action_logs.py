# File: backend/app/api/routes/user_action_logs.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import database, schemas, models # Import models juga
from app.crud import crud_user_action_log # Anda perlu membuat crud_user_action_log.py
from app.utils.security import get_current_active_superuser # Proteksi dengan Super Admin
from app.schemas.user_action_logs import UserActionLog, UserActionLogCreate # Import schema
from app.schemas.users import User # Import User untuk type hinting

router = APIRouter(
    prefix="/api/user-action-logs", # Anda bisa menyesuaikan prefix ini
    tags=["User Action Logs"]
)

@router.get("/", response_model=List[UserActionLog])
def read_all_user_action_logs(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_superuser), # Hanya admin yang bisa melihat log
    skip: int = 0, 
    limit: int = 100
):
    """Endpoint untuk mengambil semua data log aktivitas user."""
    return crud_user_action_log.get_user_action_logs(db, skip=skip, limit=limit)

# Anda bisa menambahkan endpoint POST untuk membuat log (misalnya dari middleware atau event)
# @router.post("/", response_model=UserActionLog, status_code=status.HTTP_201_CREATED)
# def create_user_action_log(
#     log: UserActionLogCreate,
#     db: Session = Depends(database.get_db),
#     current_user: User = Depends(get_current_user) # Bisa juga user biasa yang memicu log
# ):
#     """Endpoint untuk membuat log aktivitas user."""
#     # Biasanya log dibuat secara otomatis oleh sistem, bukan langsung dari frontend melalui API ini
#     return crud_user_action_log.create_user_action_log(db, log, user_id=current_user.user_id)