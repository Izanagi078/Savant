from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.tutorService import chat_tutor

router = APIRouter()

class TutorChatRequest(BaseModel):
    query: str
    request_id: str

@router.post("/chat")
async def chat_with_tutor(payload: TutorChatRequest):
    try:
        response_data = await chat_tutor(payload.query, payload.request_id)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
