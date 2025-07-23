from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime # PERBAIKAN: Impor datetime dari modul datetime

# Properti dasar yang dimiliki user
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role_id: Optional[int] = None

# Skema untuk membuat user baru (membutuhkan password)
class UserCreate(UserBase):
    password: str

# Skema untuk membaca data user dari database (respons API)
# Menyertakan semua kolom dari tabel users
class User(UserBase):
    user_id: int
    status: str
    created_at: datetime 
    updated_at: Optional[datetime] = None 
    created_by: Optional[int] = None 
    updated_by: Optional[int] = None 

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    status: Optional[str] = None
    password: Optional[str] = None