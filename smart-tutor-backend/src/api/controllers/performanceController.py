from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.dbConfig import get_db
from src.models.performance import QuizAttempt
from src.models.user import User
from src.services.authService import get_current_user

router = APIRouter()

@router.get("/history")
async def get_performance_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).order_by(QuizAttempt.timestamp.asc()).all()
        return [
            {
                "id": attempt.id,
                "topic": attempt.topic,
                "score": attempt.score,
                "total": attempt.total,
                "percentage": attempt.percentage,
                "timestamp": attempt.timestamp.isoformat() if attempt.timestamp else None
            }
            for attempt in attempts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
