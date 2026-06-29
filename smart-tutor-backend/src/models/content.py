from pydantic import BaseModel
from typing import List, Optional

class ContentIngestRequest(BaseModel):
    user_id: str
    topic: str
    level: Optional[str] = "beginner"

class ContentIngestResponse(BaseModel):
    status: str
    topic: str
    request_id: str
    syllabus: dict


