from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router
from app.api.health import router as health_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="DocuLens AI Legal Document Reader",
    description="Educational legal-style document analysis powered by OpenAI.",
    version="0.1.0",
)
"""Cross-Origin Resource Sharing. 
It is a browser security mechanism that controls whether a frontend running on one origin can make requests to a backend running on another origin"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyze_router)
