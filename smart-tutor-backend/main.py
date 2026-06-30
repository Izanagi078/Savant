from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import contentRoutes, quizRoutes, tutorRoutes, performanceRoutes, authRoutes
from src.config.dbConfig import engine, Base
from src.models.performance import QuizAttempt
from src.models.user import User
from src.models.course import Course

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for local client development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contentRoutes.router)
app.include_router(quizRoutes.router, prefix="/quiz", tags=["Quiz"])
app.include_router(tutorRoutes.router, prefix="/tutor", tags=["Tutor"])
app.include_router(performanceRoutes.router, prefix="/performance", tags=["Performance"])
app.include_router(authRoutes.router, prefix="/auth", tags=["Auth"])



