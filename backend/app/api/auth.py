from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import UserCreate, Token
from ..config.database import SessionLocal
from ..services.auth import AuthService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.register(user_in)
    access_token = service.create_access_token_for_user(user)
    return Token(access_token=access_token)

@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate(user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = service.create_access_token_for_user(user)
    return Token(access_token=access_token)
