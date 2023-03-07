from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.base_router import base_router


tags = [
    
]

app = FastAPI(
    title='Сервер',
    description='Сервер для финального приложения',
    version='0.0.1',
    openapi_tags=tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
