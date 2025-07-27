from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.crud import crud_user
from app.utils import security

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)

@router.post("/token", response_model=schemas.token.Token)
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
    refresh_token = security.create_refresh_token(data=access_token_data)

    user_response = schemas.users.User.from_orm(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user_response
    }

@router.post("/refresh")
def refresh_access_token(refresh_token: str, db: Session = Depends(database.get_db)):
    payload = security.verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = crud_user.get_user_by_username(db, username=payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    access_token_data = {
        "sub": user.username,
        "user_id": user.user_id,
        "role_id": user.role_id
    }
    new_access_token = security.create_access_token(data=access_token_data)
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
# Endpoint untuk mendapatkan data user yang sedang login
@router.get("/auth/me", response_model=schemas.users.User)
async def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    """Mendapatkan data user yang sedang login."""
    return current_user