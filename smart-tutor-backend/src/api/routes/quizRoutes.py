from fastapi import APIRouter
from src.api.controllers.quizController import generate_quiz, submit_quiz
from src.models.quiz import QuizGenerateRequest, QuizSubmitRequest, QuizGenerateResponse, QuizSubmitResponse

router = APIRouter()

@router.post("/quiz/generate", response_model=QuizGenerateResponse)
async def generate_quiz_route(payload: QuizGenerateRequest):
    return await generate_quiz(payload)

@router.post("/quiz/submit", response_model=QuizSubmitResponse)
async def submit_quiz_route(payload: QuizSubmitRequest):
    return await submit_quiz(payload)
