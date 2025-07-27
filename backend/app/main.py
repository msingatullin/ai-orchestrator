from fastapi import FastAPI
from .api import auth, data_collection, vector_db, analysis, digital_twin
from .config.database import Base, engine
from .config.settings import get_settings
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agents Ecosystem")
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(data_collection.router, prefix="/data-collection", tags=["data-collection"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(digital_twin.router, prefix="/digital-twin", tags=["digital-twin"])
app.include_router(vector_db.router, prefix="/vectors", tags=["vectors"])


@app.on_event("startup")
async def startup_event():
    try:
        redis_client = redis.from_url(settings.redis_url, encoding="utf8", decode_responses=True)
        await FastAPILimiter.init(redis_client)
    except Exception:
        # allow app startup even if Redis is unavailable (e.g., tests)
        pass
