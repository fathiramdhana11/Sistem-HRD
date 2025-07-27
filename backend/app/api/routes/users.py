from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import database, schemas
from app.crud import crud_user
from app.utils.security import get_current_active_superuser, get_current_user # Import dependencies

# Mengimpor skema secara langsung untuk menghindari 'schemas.users.User'
from app.schemas.users import User, UserCreate, UserUpdate 

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(database.get_db),
                    current_user: User = Depends(get_current_active_superuser)): # Proteksi untuk Super Admin
    """Endpoint untuk membuat user baru."""
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user_by_username = crud_user.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    return crud_user.create_user(db=db, user=user)


# Ganti dari get_current_active_superuser ke get_current_user
@router.get("/", response_model=List[User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db),
                    current_user: User = Depends(get_current_user)):  # Ubah ini
    """Endpoint untuk mengambil semua data user."""
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
def read_user_by_id(user_id: int, db: Session = Depends(database.get_db),
                    current_user: User = Depends(get_current_user)):  # Ubah dari get_current_active_superuser
    """Endpoint untuk mengambil satu user berdasarkan ID."""
    # Izinkan user melihat data diri sendiri atau superadmin melihat semua
    if current_user.user_id != user_id and current_user.role_id != 1:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to access this user data"
        )
    
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user_data(user_id: int, user_update: UserUpdate, db: Session = Depends(database.get_db),
                    current_user: User = Depends(get_current_active_superuser)): # Proteksi untuk Super Admin
    """Endpoint untuk mengupdate user."""
    updated_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db),
                    current_user: User = Depends(get_current_active_superuser)): # Proteksi untuk Super Admin
    """Endpoint untuk menghapus user."""
    success = crud_user.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return # No content returned for 204