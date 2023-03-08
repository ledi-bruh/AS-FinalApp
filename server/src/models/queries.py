from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class Queries(Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True)
    method = Column(Enum('GET', 'POST', 'PUT', 'DELETE', name='methods_enum'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_guid = Column(GUID, ForeignKey('users.guid'), nullable=False)
