from fastapi import APIRouter
from src.api.controllers import authController

router = APIRouter()
router.include_router(authController.router)
