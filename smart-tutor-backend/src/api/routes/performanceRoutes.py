from fastapi import APIRouter
from src.api.controllers.performanceController import router as performance_router

router = APIRouter()
router.include_router(performance_router)
