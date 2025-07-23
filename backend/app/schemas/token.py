from pydantic import BaseModel
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

# Menggunakan tokenUrl yang sesuai dengan endpoint login Anda
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional['User'] = None # Untuk menyertakan data user saat login

class TokenData(BaseModel):
    username: Optional[str] = None
    
# Import User schema secara lokal untuk menghindari circular import jika User ada di schemas/users.py
from .users import User 
Token.update_forward_refs() # Perbarui referensi ke skema User