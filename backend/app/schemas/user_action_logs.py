# Asumsi lokasi: backend/app/schemas/user_action_logs.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime # PERBAIKAN: Impor datetime dari modul datetime

class UserActionLogBase(BaseModel):
    user_id: Optional[int] = None
    menu_id: Optional[int] = None
    terminal_name: Optional[str] = None
    action: Optional[str] = None
    target_id: Optional[int] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    device_info: Optional[str] = None

class UserActionLogCreate(UserActionLogBase):
    pass

class UserActionLog(UserActionLogBase):
    log_id: int
    created_at: datetime

    class Config:
        from_attributes = True