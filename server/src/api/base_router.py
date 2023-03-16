from fastapi import APIRouter
from src.api import auth, users, queries, ml


base_router = APIRouter()
base_router.include_router(auth.router)
base_router.include_router(users.router)
base_router.include_router(queries.router)
base_router.include_router(ml.router)
