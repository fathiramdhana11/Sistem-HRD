from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(login: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login.username).first()
    if not user or not verify_password(login.password, user.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")

    token = create_access_token(data={"sub": user.username})

    return {
        "token": token,
        "user": {
            "user_id": user.user_id,
            "username": user.username,
        }
    }
