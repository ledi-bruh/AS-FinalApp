from src.services.auth import get_current_user
from src.utils.role_checker import RoleChecker
from src.utils.query_logger import QueryLogger


AUTHORIZED = get_current_user
ADMIN_ONLY = RoleChecker(['admin'])
QUERY_LOGGER = QueryLogger()
