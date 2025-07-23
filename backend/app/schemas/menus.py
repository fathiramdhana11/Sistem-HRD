# File: backend/app/schemas/menu.py

from pydantic import BaseModel
from typing import List, Optional

# Skema dasar
class MenuBase(BaseModel):
    menu_name: str
    route: Optional[str] = None
    icon: Optional[str] = None
    order_no: int
    is_active: bool
    parent_menu_id: Optional[int] = None

class MenuCreate(MenuBase):
    pass

# Skema untuk dibaca dari database
class Menu(MenuBase):
    menu_id: int

    class Config:
        from_attributes = True

# Skema ini bisa berisi submenu di dalamnya
class MenuWithSubMenu(Menu):
    sub_menus: List['MenuWithSubMenu'] = []

# Ini penting untuk Pydantic agar bisa menangani rekursi
MenuWithSubMenu.update_forward_refs()