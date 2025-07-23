# File: backend/app/schemas/token.py

from pydantic import BaseModel
from typing import Optional
from .users import User

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User 

class TokenData(BaseModel):
    username: Optional[str] = None