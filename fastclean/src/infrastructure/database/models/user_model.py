from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from ..database import Base


class UserModel(Base):
    """SQLAlchemy User Model"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)