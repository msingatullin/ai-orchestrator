from sqlalchemy.orm import Session
from uuid import uuid4
from ..models import User
from ..schemas import UserCreate
from ..core.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_in: UserCreate) -> User:
        user = User(
            id=str(uuid4()),
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            organization_id=user_in.organization_id,
            role=user_in.role or "user",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
