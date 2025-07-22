from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)  # Optional
    status = Column(String, default='active')
    role_id = Column(Integer)
    created_at = Column(TIMESTAMP)
