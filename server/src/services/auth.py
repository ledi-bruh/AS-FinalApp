from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.core.settings import settings
from src.models.users import Users
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.secure import SecureService


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(token: str = Depends(oauth2_schema)) -> dict:
    return AuthService.decode_token(token)


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def encode_token(user_guid: str, user_role: str) -> JwtToken:
        now = datetime.now(timezone.utc)
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'user_guid': str(user_guid),
            'user_role': user_role
        }
        
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        
        return JwtToken(access_token=token)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')
        
        return {
            'guid': payload.get('user_guid'),
            'role': payload.get('user_role')
        }
    
    def login(self, login: str, password_text: str) -> JwtToken:
        user: Users = (
            self.session
            .query(Users)
            .filter(Users.login == login)
            .first()
        )
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not SecureService.verify_password(password_text, user.password_hashed):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return self.encode_token(user.guid, user.role)
