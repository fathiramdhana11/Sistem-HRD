# File: backend/app/api/routes/menus.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Pastikan semua impor ini sudah benar
from ... import models, schemas, database
# Tambahkan import untuk security
from app.utils import security

# !! INI BAGIAN YANG HILANG ATAU PERLU DIPERBAIKI !!
# Mendefinisikan variabel 'router' yang akan dipanggil oleh api_router.py
router = APIRouter(
    prefix="/api/menus",
    tags=['Menus']
)

# Helper function untuk mengubah data flat menjadi struktur pohon (hirarkis)
def build_menu_tree(menus: List[models.Menu]) -> List[schemas.Menu]:
    # Buat map dari semua menu yang accessible
    accessible_menu_ids = {menu.menu_id for menu in menus}
    menu_map = {menu.menu_id: schemas.Menu.from_orm(menu) for menu in menus}
    tree = []

    for menu_id, menu_node in menu_map.items():
        if menu_node.parent_menu_id:
            # Hanya tambahkan ke parent jika parent juga accessible
            parent = menu_map.get(menu_node.parent_menu_id)
            if parent and menu_node.parent_menu_id in accessible_menu_ids:
                parent.sub_menus.append(menu_node)
            elif menu_node.parent_menu_id not in accessible_menu_ids:
                # Jika parent tidak accessible, jadikan sebagai root menu
                tree.append(menu_node)
        else:
            tree.append(menu_node)
    
    # Mengurutkan menu utama dan submenu berdasarkan order_no
    tree.sort(key=lambda x: x.order_no)
    for node in menu_map.values():
        node.sub_menus.sort(key=lambda x: x.order_no)
        
    return tree

# Tambahkan endpoint /tree yang hilang
@router.get("/tree", response_model=List[schemas.Menu])
def get_all_menus_as_tree(db: Session = Depends(database.get_db)):
    """
    Mengambil semua menu yang aktif dan mengembalikannya dalam format hirarkis (pohon)
    berdasarkan parent_menu_id. Endpoint ini digunakan untuk RoleAccessView.
    """
    all_menus = db.query(models.Menu).filter(models.Menu.is_active == True).order_by(models.Menu.order_no).all()
    if not all_menus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active menus found")
    
    return build_menu_tree(all_menus)

@router.get("/user-menus", response_model=List[schemas.Menu])
def get_user_menus(db: Session = Depends(database.get_db), current_user: models.User = Depends(security.get_current_user)):
    """
    Mengambil menu yang dapat diakses oleh pengguna berdasarkan role_id mereka.
    """
    # Dapatkan role_id dari user yang sedang login
    role_id = current_user.role_id
    
    # Dapatkan semua menu yang aktif
    all_menus = db.query(models.Menu).filter(models.Menu.is_active == True).all()
    
    # Jika superadmin (role_id = 1), kembalikan semua menu
    if role_id == 1:  # Sesuaikan dengan role_id superadmin di sistem Anda
        return build_menu_tree(all_menus)
    
    # Dapatkan menu_id yang dapat diakses oleh role ini
    accessible_menu_ids = db.query(models.RoleMenuAccess.menu_id).filter(
        models.RoleMenuAccess.role_id == role_id
    ).all()
    accessible_menu_ids = [menu_id for (menu_id,) in accessible_menu_ids]
    
    # Filter menu yang dapat diakses
    accessible_menus = [menu for menu in all_menus if menu.menu_id in accessible_menu_ids]
    
    # Tambahkan parent menu yang diperlukan untuk struktur tree yang benar
    # Cari parent menu yang diperlukan untuk child menu yang accessible
    required_parent_ids = set()
    for menu in accessible_menus:
        if menu.parent_menu_id and menu.parent_menu_id not in accessible_menu_ids:
            required_parent_ids.add(menu.parent_menu_id)
    
    # Tambahkan parent menu yang diperlukan ke accessible_menus
    if required_parent_ids:
        parent_menus = db.query(models.Menu).filter(
            models.Menu.menu_id.in_(required_parent_ids),
            models.Menu.is_active == True
        ).all()
        accessible_menus.extend(parent_menus)
    
    return build_menu_tree(accessible_menus)