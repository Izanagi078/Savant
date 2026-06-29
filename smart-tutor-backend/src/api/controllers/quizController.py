from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.quizService import generate_quiz

router = APIRouter()

class QuizGenerateRequest(BaseModel):
    topic: str
    count: int = 4

class QuizSubmitRequest(BaseModel):
    answers: dict  # { "question_id": selected_index }
    correct_answers: dict  # { "question_id": correct_index }

@router.post("/generate")
async def get_quiz(payload: QuizGenerateRequest):
    try:
        quiz_data = await generate_quiz(payload.topic, payload.count)
        return quiz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
async def submit_quiz(payload: QuizSubmitRequest):
    score = 0
    total = len(payload.correct_answers)
    detailed_results = []
    
    for qid, ans in payload.answers.items():
        correct_ans = payload.correct_answers.get(str(qid)) or payload.correct_answers.get(int(qid))
        is_correct = (ans == correct_ans)
        if is_correct:
            score += 1
        detailed_results.append({
            "question_id": qid,
            "user_answer": ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct
        })
        
    return {
        "score": score,
        "total": total,
        "results": detailed_results
    }
