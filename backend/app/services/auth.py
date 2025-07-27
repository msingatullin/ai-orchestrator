from datetime import timedelta, datetime
from uuid import uuid4
from sqlalchemy.orm import Session
from ..models import User, RefreshToken
from ..schemas import UserCreate
from ..core.security import verify_password, create_access_token, create_refresh_token
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
        return create_access_token(subject=user.id, role=user.role, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))

    def create_refresh_token_for_user(self, user: User) -> RefreshToken:
        token = create_refresh_token(subject=user.id, role=user.role)
        rt = RefreshToken(
            id=str(uuid4()),
            token=token,
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
        self.db.add(rt)
        self.db.commit()
        self.db.refresh(rt)
        return rt

    def register(self, user_in: UserCreate) -> User:
        return self.user_service.create_user(user_in)

    def get_refresh_token(self, token: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
