# File: backend/app/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Sekarang impor ini akan berfungsi dengan benar
from app import database, models, schemas
from app.crud import crud_user
from app.utils import security

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)

# Pemanggilan schemas.Token sekarang valid
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud_user.get_user_by_username(db, username=form_data.username)

    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_data = {
        "sub": user.username,
        "user_id": user.user_id,
        "role_id": user.role_id
    }
    access_token = security.create_access_token(data=access_token_data)

    # Pemanggilan schemas.User sekarang juga valid
    user_response = schemas.User.from_orm(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }