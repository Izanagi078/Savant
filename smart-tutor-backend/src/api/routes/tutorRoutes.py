from fastapi import APIRouter
from src.api.controllers import tutorController

router = APIRouter()
router.include_router(tutorController.router)
