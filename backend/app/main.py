from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import judge, rubrics, submissions
from app.config import get_settings
from app.database import init_models

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

app = FastAPI(title="JudgeAI", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(submissions.router)
app.include_router(rubrics.router)
app.include_router(judge.router)

@app.get("/health")
async def health():
    return {"status": "ok"}