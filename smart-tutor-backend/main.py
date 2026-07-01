from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import contentRoutes, quizRoutes, tutorRoutes, performanceRoutes, authRoutes
from src.config.dbConfig import engine, Base
from src.models.performance import QuizAttempt
from src.models.user import User
from src.models.course import Course
from src.models.chat import ChatSession

from contextlib import asynccontextmanager

import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Connected to PostgreSQL successfully!")
    yield

app = FastAPI(lifespan=lifespan)

# Enable CORS with explicit origins for cookie credential transmission
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([o.strip() for o in env_origins.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contentRoutes.router)
app.include_router(quizRoutes.router, prefix="/quiz", tags=["Quiz"])
app.include_router(tutorRoutes.router, prefix="/tutor", tags=["Tutor"])
app.include_router(performanceRoutes.router, prefix="/performance", tags=["Performance"])
app.include_router(authRoutes.router, prefix="/auth", tags=["Auth"])



