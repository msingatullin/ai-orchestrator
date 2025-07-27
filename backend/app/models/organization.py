from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from .base import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
