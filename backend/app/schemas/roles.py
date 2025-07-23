from pydantic import BaseModel
from typing import Optional
from datetime import datetime # PERBAIKAN: Impor datetime dari modul datetime

class RoleBase(BaseModel):
    role_name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    role_id: int
    created_at: datetime 
    updated_at: Optional[datetime] = None 
    created_by: Optional[int] = None 
    updated_by: Optional[int] = None 

    class Config:
        from_attributes = True