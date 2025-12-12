from fastapi import APIRouter
from src.api.controllers import contentController

router = APIRouter()
router.include_router(contentController.router, prefix="/content", tags=["Content"])
