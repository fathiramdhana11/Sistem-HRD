from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MenuBase(BaseModel):
    menu_name: str
    route: Optional[str] = None
    parent_menu_id: Optional[int] = None
    icon: Optional[str] = None
    order_no: Optional[int] = 0
    is_active: Optional[bool] = True

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    menu_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    # Untuk struktur pohon menu
    children: List['Menu'] = [] 

    class Config:
        from_attributes = True

class MenuUpdate(BaseModel):
    menu_name: Optional[str] = None
    route: Optional[str] = None
    parent_menu_id: Optional[int] = None
    icon: Optional[str] = None
    order_no: Optional[int] = None # Bisa diupdate
    is_active: Optional[bool] = None # Bisa diupdate

Menu.update_forward_refs()