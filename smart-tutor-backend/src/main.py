from fastapi import FastAPI
from src.api.routes import contentRoutes, quizRoutes

app = FastAPI()
app.include_router(contentRoutes.router)
app.include_router(quizRoutes.router, prefix="/quiz")
