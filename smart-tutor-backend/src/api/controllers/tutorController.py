from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.config.dbConfig import get_db
from src.models.user import User
from src.services.authService import get_current_user
from src.services.tutorService import chat_tutor

router = APIRouter()

class TutorChatRequest(BaseModel):
    query: str
    request_id: str

@router.post("/chat")
async def chat_with_tutor(
    payload: TutorChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        response_data = await chat_tutor(payload.query, payload.request_id, current_user.id, db)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
