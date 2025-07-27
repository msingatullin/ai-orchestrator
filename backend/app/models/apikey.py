from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(String, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
