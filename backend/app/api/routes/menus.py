# File: backend/app/api/routes/menus.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Pastikan semua impor ini sudah benar
from ... import models, schemas, database

# !! INI BAGIAN YANG HILANG ATAU PERLU DIPERBAIKI !!
# Mendefinisikan variabel 'router' yang akan dipanggil oleh api_router.py
router = APIRouter(
    prefix="/api/menus",
    tags=['Menus']
)

# Helper function untuk mengubah data flat menjadi struktur pohon (hirarkis)
def build_menu_tree(menus: List[models.Menu]) -> List[schemas.MenuWithSubMenu]:
    menu_map = {menu.menu_id: schemas.MenuWithSubMenu.from_orm(menu) for menu in menus}
    tree = []

    for menu_id, menu_node in menu_map.items():
        if menu_node.parent_menu_id:
            parent = menu_map.get(menu_node.parent_menu_id)
            if parent:
                parent.sub_menus.append(menu_node)
        else:
            tree.append(menu_node)
    
    # Mengurutkan menu utama dan submenu berdasarkan order_no
    tree.sort(key=lambda x: x.order_no)
    for node in menu_map.values():
        node.sub_menus.sort(key=lambda x: x.order_no)
        
    return tree

# Pastikan decorator endpoint menggunakan variabel 'router' yang baru dibuat
@router.get("/tree", response_model=List[schemas.MenuWithSubMenu])
def get_all_menus_as_tree(db: Session = Depends(database.get_db)):
    """
    Mengambil semua menu yang aktif dan mengembalikannya dalam format hirarkis (pohon)
    berdasarkan parent_menu_id.
    """
    all_menus = db.query(models.Menu).filter(models.Menu.is_active == True).order_by(models.Menu.order_no).all()
    if not all_menus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active menus found")
    
    return build_menu_tree(all_menus)