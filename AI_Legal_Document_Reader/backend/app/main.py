from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.observability import router as observability_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="AI Legal Document Reader",
    description="Educational legal-style document analysis with LangChain, RAG, and observability.",
    version="6.0.0-preview",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(analyze_router)
app.include_router(observability_router)
