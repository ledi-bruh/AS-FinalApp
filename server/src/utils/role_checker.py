from fastapi import Depends, HTTPException, status
from src.services.auth import get_current_user


class RoleChecker:
    """
        Предоставляет доступ определенным ролям.
    """

    def __init__(self, allowed_roles: list):
        self.allowed = allowed_roles

    def __call__(self, user_info: dict = Depends(get_current_user)):
        role = user_info.get('role')

        if role not in self.allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Недостаточно прав',
            )
