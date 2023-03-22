from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.services.queries import QueriesService
from src.dependencies import ADMIN_ONLY


router = APIRouter(
    prefix='/queries',
    tags=['queries'],
    dependencies=[Depends(ADMIN_ONLY)]
)


@router.get('/', name='Получить все запросы')
def get(service: QueriesService = Depends()):
    return service.all()


@router.get('/{id}', name='Получить запрос по id')
def get(id: int, service: QueriesService = Depends()):
    return service.get(id)


@router.get('/u/{user_guid}', name='Получить запросы по guid пользователя')
def get(user_guid: UUID4, service: QueriesService = Depends()):
    return service.get_by_user(user_guid)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить запрос')
def delete(id: int, service: QueriesService = Depends()):
    return service.delete(id)
