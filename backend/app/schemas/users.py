# File: backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

# Properti dasar yang dimiliki user
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role_id: Optional[int] = None

# Skema untuk membuat user baru (membutuhkan password)
class UserCreate(UserBase):
    password: str

# Skema untuk membaca data user dari database (respons API)
# Tidak menyertakan password demi keamanan
class User(UserBase):
    user_id: int
    status: str

    class Config:
        from_attributes = True # Memungkinkan Pydantic membaca data dari objek SQLAlchemy

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    status: Optional[str] = None