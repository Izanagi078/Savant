from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.services.quizService import generate_quiz
from src.config.dbConfig import get_db
from src.models.performance import QuizAttempt
from src.models.user import User
from src.services.authService import get_current_user

router = APIRouter()

class QuizGenerateRequest(BaseModel):
    topic: str
    count: int = 10
    level: str = "Beginner"

class QuizSubmitRequest(BaseModel):
    topic: str = "General"
    answers: dict  # { "question_id": selected_index }
    correct_answers: dict  # { "question_id": correct_index }

@router.post("/generate")
async def get_quiz(
    payload: QuizGenerateRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        quiz_data = await generate_quiz(payload.topic, payload.count, payload.level)
        return quiz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
async def submit_quiz(
    payload: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    score = 0
    total = len(payload.correct_answers)
    detailed_results = []
    
    for qid, ans in payload.answers.items():
        correct_ans = payload.correct_answers.get(str(qid))
        if correct_ans is None:
            correct_ans = payload.correct_answers.get(int(qid))
        
        is_correct = (ans == correct_ans)
        if is_correct:
            score += 1
        detailed_results.append({
            "question_id": qid,
            "user_answer": ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct
        })
    
    percentage = (score / total * 100) if total > 0 else 0.0
    
    # Save attempt into the database
    try:
        attempt = QuizAttempt(
            user_id=current_user.id,
            topic=payload.topic,
            score=score,
            total=total,
            percentage=percentage
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
    except Exception as e:
        # Log database error and return results anyway (graceful degradation)
        print(f"Database error writing attempt: {e}")
        
    return {
        "score": score,
        "total": total,
        "results": detailed_results
    }

