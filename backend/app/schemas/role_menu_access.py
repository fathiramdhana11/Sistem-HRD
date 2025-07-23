# Asumsi lokasi: backend/app/schemas/role_menu_access.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime # PERBAIKAN: Impor datetime dari modul datetime

class RoleMenuAccessBase(BaseModel):
    role_id: int
    menu_id: int

class RoleMenuAccessCreate(RoleMenuAccessBase):
    pass

class RoleMenuAccess(RoleMenuAccessBase):
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True