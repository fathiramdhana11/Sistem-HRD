# File: backend/app/api/routes/roles.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import database, schemas
from app.crud import crud_role
# Fix: Import both functions
from app.utils.security import get_current_active_superuser, get_current_user

router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"]
)

@router.get("/", response_model=List[schemas.roles.Role])
def read_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db),
                current_user: schemas.users.User = Depends(get_current_user)):  # Ubah ini
    """Endpoint untuk mengambil semua data role."""
    roles = crud_role.get_all_roles(db, skip=skip, limit=limit)
    return roles

@router.post("/", response_model=schemas.roles.Role)
def create_role(role: schemas.roles.RoleCreate, db: Session = Depends(database.get_db),
                current_user: schemas.users.User = Depends(get_current_user)):  # Ubah ini
    """Endpoint untuk membuat role baru."""
    return crud_role.create_role(db=db, role=role)

@router.put("/{role_id}", response_model=schemas.roles.Role)
def update_role(role_id: int, role: schemas.roles.RoleCreate, db: Session = Depends(database.get_db),
                current_user: schemas.users.User = Depends(get_current_active_superuser)):
    """Endpoint untuk mengupdate role."""
    db_role = crud_role.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return crud_role.update_role(db=db, role_id=role_id, role=role)

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(database.get_db),
                current_user: schemas.users.User = Depends(get_current_active_superuser)):
    """Endpoint untuk menghapus role."""
    db_role = crud_role.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return crud_role.delete_role(db=db, role_id=role_id)