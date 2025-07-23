# Asumsi lokasi: backend/app/models/user_action_logs.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class UserActionLog(Base):
    __tablename__ = "user_action_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    menu_id = Column(Integer, ForeignKey("menus.menu_id", ondelete="SET NULL"))
    terminal_name = Column(String(50))
    action = Column(String(50))
    target_id = Column(Integer)
    description = Column(Text)
    ip_address = Column(String(45))
    device_info = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Relasi ke tabel users dan menus
    user = relationship("User", foreign_keys=[user_id])
    menu = relationship("Menu", foreign_keys=[menu_id])