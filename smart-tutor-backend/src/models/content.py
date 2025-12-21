from pydantic import BaseModel
from typing import List, Optional

class ContentIngestRequest(BaseModel):
    user_id: str
    topic: str
    level: Optional[str] = "beginner"
    context: Optional[str] = ""

class ContentIngestResponse(BaseModel):
    status: str
    topic: str
    request_id: str
    videos: List[dict]
    papers: List[dict]
    resources: List[dict]
