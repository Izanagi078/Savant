from fastapi import FastAPI
from src.api.routes import contentRoutes

app = FastAPI()
app.include_router(contentRoutes.router)
