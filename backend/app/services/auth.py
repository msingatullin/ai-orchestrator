from datetime import timedelta
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate
from ..core.security import verify_password, create_access_token
from .user import UserService
from ..config.settings import get_settings

settings = get_settings()

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.user_service.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token_for_user(self, user: User) -> str:
        return create_access_token(subject=user.id, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))

    def register(self, user_in: UserCreate) -> User:
        return self.user_service.create_user(user_in)
