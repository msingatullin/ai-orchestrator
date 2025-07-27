from uuid import uuid4
from sqlalchemy.orm import Session
from ..models import APIKey, User

class APIKeyService:
    def __init__(self, db: Session):
        self.db = db

    def create_key_for_user(self, user: User) -> APIKey:
        key = APIKey(id=str(uuid4()), key=str(uuid4()), user_id=user.id)
        self.db.add(key)
        self.db.commit()
        self.db.refresh(key)
        return key

    def get_key(self, key: str) -> APIKey | None:
        return self.db.query(APIKey).filter(APIKey.key == key).first()
