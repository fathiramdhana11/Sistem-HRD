# File: backend/app/api/routes/role_menu_access.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import database, schemas, models # Import models juga
from app.crud import crud_role_menu_access # Import CRUD logic
from app.utils.security import get_current_active_superuser # Proteksi dengan Super Admin
from app.schemas.role_menu_access import RoleMenuAccess, RoleMenuAccessCreate # Import schema
from app.schemas.users import User # Import User untuk type hinting

router = APIRouter(
    prefix="/api/role-menu-access", # Anda bisa menyesuaikan prefix ini
    tags=["Role Menu Access"]
)

@router.get("/", response_model=List[RoleMenuAccess])
def read_all_role_menu_access(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Endpoint untuk mengambil semua data akses menu peran."""
    return crud_role_menu_access.get_all_role_menu_access(db)

@router.post("/", response_model=RoleMenuAccess, status_code=status.HTTP_201_CREATED)
def create_role_menu_access(
    role_menu_access: RoleMenuAccessCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Endpoint untuk memberikan akses menu baru ke peran."""
    db_access = crud_role_menu_access.get_role_menu_access_by_ids(
        db, role_id=role_menu_access.role_id, menu_id=role_menu_access.menu_id
    )
    if db_access:
        raise HTTPException(status_code=400, detail="Role already has access to this menu")
    
    # Anda mungkin ingin mengisi created_by/updated_by di CRUD
    return crud_role_menu_access.create_role_menu_access(db, role_menu_access)

@router.delete("/{role_id}/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_menu_access(
    role_id: int,
    menu_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Endpoint untuk menghapus akses menu dari peran."""
    success = crud_role_menu_access.delete_role_menu_access(db, role_id, menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role menu access not found")
    return