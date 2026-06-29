from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import contentRoutes, quizRoutes, tutorRoutes

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


