from fastapi import APIRouter

from app.api.api_v1.endpoints import job, service

api_router = APIRouter()
api_router.include_router(job.router, prefix="/job", tags=["job"])
api_router.include_router(service.router, prefix="/service", tags=["service"])
