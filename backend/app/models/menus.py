# File: backend/app/models/menu.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from ..database import Base

class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String, nullable=False)
    route = Column(String)
    parent_menu_id = Column(Integer, ForeignKey("menus.menu_id"))
    icon = Column(String)
    order_no = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    updated_by = Column(Integer, ForeignKey("users.user_id"))