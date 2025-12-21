from pydantic import BaseModel

class article(BaseModel):
    title: str
    url: str
    snippet: str
    score: float
