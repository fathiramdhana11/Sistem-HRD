from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow) # Tambahkan onupdate
    created_by = Column(Integer, ForeignKey("users.user_id", name="fk_roles_created_by")) # Tambah FK
    updated_by = Column(Integer, ForeignKey("users.user_id", name="fk_roles_updated_by")) # Tambah FK

    # Mendefinisikan relasi balik ke tabel 'users' dengan foreign_keys yang spesifik
    users = relationship("User", back_populates="role", foreign_keys="User.role_id")

    # Relasi untuk created_by dan updated_by
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])