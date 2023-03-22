from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.settings import settings
from src.api.base_router import base_router


tags = [
    {
        "name": "auth",
        "description": "Вход в админ-панель"
    },
    {
        "name": "users",
        "description": "Управление пользователями"
    },
    {
        "name": "queries",
        "description": "Взаимодействиями с историей запросов"
    },
    {
        "name": "ml",
        "description": "Взаимодействие с моделью машинного обучения"
    },
]

app = FastAPI(
    title='Сервер',
    description='Сервер для финального приложения',
    version='1.0.0',
    openapi_tags=tags,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_url],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["*"],
)

app.include_router(base_router)
