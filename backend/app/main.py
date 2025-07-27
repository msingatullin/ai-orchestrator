from fastapi import FastAPI
from .api import auth
from .config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agents Ecosystem")
app.include_router(auth.router, prefix="/auth", tags=["auth"])
