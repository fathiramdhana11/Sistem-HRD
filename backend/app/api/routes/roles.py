# File: backend/app/api/routes/roles.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import database, schemas
from app.crud import crud_role
from app.utils.security import get_current_active_superuser # Proteksi dengan Super Admin

router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"]
)

@router.get("/", response_model=List[schemas.roles.Role])
def read_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db),
                  current_user: schemas.users.User = Depends(get_current_active_superuser)): # Proteksi untuk Super Admin
    """Endpoint untuk mengambil semua data role."""
    roles = crud_role.get_all_roles(db, skip=skip, limit=limit)
    return roles

# Anda bisa menambahkan endpoint POST, PUT, DELETE untuk roles jika diperlukan