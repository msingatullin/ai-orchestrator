from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..schemas import UserCreate, Token
from ..config.database import SessionLocal
from ..services.auth import AuthService
from fastapi_limiter.depends import RateLimiter
from ..config.settings import get_settings

settings = get_settings()
from ..models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

rate_dep = [Depends(RateLimiter(times=5, seconds=60))] if settings.redis_url else []

@router.post("/register", response_model=Token, dependencies=rate_dep)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.register(user_in)
    access_token = service.create_access_token_for_user(user)
    refresh = service.create_refresh_token_for_user(user)
    return Token(access_token=access_token, refresh_token=refresh.token)

@router.post("/login", response_model=Token, dependencies=rate_dep)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate(user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = service.create_access_token_for_user(user)
    refresh = service.create_refresh_token_for_user(user)
    return Token(access_token=access_token, refresh_token=refresh.token)


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    rt = service.get_refresh_token(refresh_token)
    if not rt or rt.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user = db.query(User).get(rt.user_id)
    access_token = service.create_access_token_for_user(user)
    new_refresh = service.create_refresh_token_for_user(user)
    return Token(access_token=access_token, refresh_token=new_refresh.token)
