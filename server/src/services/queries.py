from typing import List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.queries import Queries


class QueriesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Queries]:
        queries = (
            self.session
            .query(Queries)
            .all()
        )
        return queries

    def get(self, id: int) -> Queries:
        query = (
            self.session
            .query(Queries)
            .filter(Queries.id == id)
            .first()
        )

        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запрос отсутствует')

        return query

    def get_by_user(self, user_guid: str) -> List[Queries]:
        queries = (
            self.session
            .query(Queries)
            .filter(Queries.user_guid == user_guid)
            .all()
        )

        if not queries:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Подобные запросы отсутствуют')

        return queries

    def delete(self, id: int) -> None:
        query = self.get(id)
        self.session.delete(query)
        self.session.commit()
