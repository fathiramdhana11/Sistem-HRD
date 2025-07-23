# Asumsi lokasi: backend/app/models/menus.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String(100), nullable=False)
    route = Column(String(150))
    parent_menu_id = Column(Integer, ForeignKey("menus.menu_id", ondelete="CASCADE"))
    icon = Column(String(100))
    order_no = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    updated_by = Column(Integer, ForeignKey("users.user_id"))

    # Self-referential relationship for parent/child menus
    parent = relationship("Menu", remote_side=[menu_id], backref="children")

    # Relasi untuk created_by dan updated_by
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])