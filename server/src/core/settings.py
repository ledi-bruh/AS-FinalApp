from pydantic import BaseSettings
from src.utils.pattern import singleton


@singleton
class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 9999
    docs_url: str = '/docs'
    redoc_url: str = '/redoc'

    client_url: str = '*'

    db_login: str
    db_password: str
    db_host: str
    db_port: int
    db_database: str
    db_schema: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_seconds: int

    admin_login: str
    admin_password: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
