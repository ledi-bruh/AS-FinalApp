from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.models.base import Base


class Users(Base):
    __tablename__ = 'users'
    guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    login = Column(String, nullable=False, unique=True)
    password_hashed = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
