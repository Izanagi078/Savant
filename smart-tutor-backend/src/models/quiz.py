from pydantic import BaseModel
from typing import List, Dict

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    answer: str

class QuizGenerateRequest(BaseModel):
    request_id: str
    user_id: str

class QuizGenerateResponse(BaseModel):
    request_id: str
    topic: str
    questions: List[QuizQuestion]

class QuizSubmitRequest(BaseModel):
    request_id: str
    user_id: str
    answers: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "request_id": "abc123",
                "user_id": "u001",
                "answers": {
                    "q1": "B",
                    "q2": "D",
                    "q3": "A"
                }
            }
        }

class QuizSubmitResponse(BaseModel):
    score: int
    total: int
    correct_answers: Dict[str, bool]
