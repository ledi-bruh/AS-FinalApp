from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from src.core.settings import settings


metadata = MetaData(schema=settings.db_schema)

Base = declarative_base(metadata=metadata)
