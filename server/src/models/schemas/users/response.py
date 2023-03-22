from pydantic import BaseModel, UUID4
from datetime import datetime


class UsersResponse(BaseModel):
    guid: UUID4
    login: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
