from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.crud import crud_user

# Ganti ini dengan kunci rahasia yang kuat dari variabel lingkungan!
SECRET_KEY = "b6fd8fbc4727bf95abb2379ca284166501d00b514506feba78b7b4e8862c21c0"  # Ganti dengan kunci rahasia yang kuat dan unik
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ID peran Super Admin Anda
SUPER_ADMIN_ROLE_ID = 1 # Sesuaikan dengan role_id super admin di database Anda (misalnya, 1 untuk Super Admin)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependensi untuk mendapatkan user yang sedang login dari token
async def get_current_user(token: str = Depends(schemas.token.oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # TokenData didefinisikan di schemas/token.py
        token_data = schemas.token.TokenData(username=username) 
    except JWTError:
        raise credentials_exception
    user = crud_user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Dependensi untuk mendapatkan user yang sedang login dan memastikan mereka adalah Super Admin
async def get_current_active_superuser(current_user: models.User = Depends(get_current_user)):
    if current_user.role_id != SUPER_ADMIN_ROLE_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges to perform this action"
        )
    return current_user