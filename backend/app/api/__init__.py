from fastapi import APIRouter
from . import auth, data_collection, vector_db, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(data_collection.router, prefix="/data-collection", tags=["data-collection"])
api_router.include_router(vector_db.router, prefix="/vectors", tags=["vectors"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
