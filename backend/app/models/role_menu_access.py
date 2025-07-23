# Asumsi lokasi: backend/app/models/role_menu_access.py
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class RoleMenuAccess(Base):
    __tablename__ = "role_menu_access"

    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    updated_by = Column(Integer, ForeignKey("users.user_id"))

    __table_args__ = (
        PrimaryKeyConstraint('role_id', 'menu_id'), # Menetapkan primary key gabungan
    )

    # Relasi ke tabel roles dan menus
    role = relationship("Role")
    menu = relationship("Menu")

    # Relasi untuk created_by dan updated_by
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])