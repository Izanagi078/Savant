from fastapi import APIRouter
from src.api.controllers import quizController

router = APIRouter()
router.include_router(quizController.router)
