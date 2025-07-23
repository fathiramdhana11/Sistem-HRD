# File: backend/app/api/routes/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import database, schemas
from app.crud import crud_user

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Endpoint untuk membuat user baru."""
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user_by_username = crud_user.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Memanggil fungsi dari crud_user untuk membuat user
    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Endpoint untuk mengambil semua data user."""
    # Memanggil fungsi dari crud_user untuk mengambil users
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    """Endpoint untuk mengambil satu user berdasarkan ID."""
    # Memanggil fungsi dari crud_user untuk mengambil user
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.user.User)
def update_user_data(user_id: int, user_update: schemas.user.UserUpdate, db: Session = Depends(database.get_db)):
    """Endpoint untuk mengupdate user."""
    updated_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user