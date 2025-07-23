# File: backend/app/schemas/role.py

from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    role_name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    role_id: int

    class Config:
        from_attributes = True