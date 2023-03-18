from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 9998
    debug: bool = False
    backend_url: str
    
    loc_access_token: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
