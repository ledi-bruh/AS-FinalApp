from datetime import datetime, timezone
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.queries import Queries
from src.services.auth import get_current_user


class QueryLogger:
    """
        Логирует запросы в базу данных.
    """

    def __call__(self, request: Request, user_info: dict = Depends(get_current_user), session: Session = Depends(get_session)):
        query = Queries(
            method=request.method,
            url=str(request.url),
            user_guid=user_info.get('guid'),
            created_at=datetime.now(timezone.utc)
        )
        session.add(query)
        session.commit()
