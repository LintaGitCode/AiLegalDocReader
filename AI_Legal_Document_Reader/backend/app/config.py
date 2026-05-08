import os
from functools import lru_cache


class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "50000"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1200"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))
    max_retrieved_chunks: int = int(os.getenv("MAX_RETRIEVED_CHUNKS", "6"))
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    observability_enabled: bool = os.getenv("OBSERVABILITY_ENABLED", "true").lower() == "true"


@lru_cache
def get_settings() -> Settings:
    return Settings()
