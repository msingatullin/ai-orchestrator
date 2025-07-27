from fastapi import APIRouter
from . import auth, data_collection, vector_db, analysis, digital_twin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(data_collection.router, prefix="/data-collection", tags=["data-collection"])
api_router.include_router(vector_db.router, prefix="/vectors", tags=["vectors"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(digital_twin.router, prefix="/digital-twin", tags=["digital-twin"])
