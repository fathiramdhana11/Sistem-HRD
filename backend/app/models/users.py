from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    status = Column(String(20), default='active')
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow) # Tambahkan onupdate
    created_by = Column(Integer, ForeignKey("users.user_id", name="fk_users_created_by")) # Tambah FK
    updated_by = Column(Integer, ForeignKey("users.user_id", name="fk_users_updated_by")) # Tambah FK

    # Mendefinisikan relasi ke tabel 'roles' dengan foreign_keys yang spesifik
    role = relationship("Role", back_populates="users", foreign_keys=[role_id])

    # Relasi untuk created_by dan updated_by (self-referential relationship)
    # Penting: Gunakan remote_side untuk menghindari ambiguitas
    creator = relationship("User", remote_side=[user_id], foreign_keys=[created_by], post_update=True)
    updater = relationship("User", remote_side=[user_id], foreign_keys=[updated_by], post_update=True)