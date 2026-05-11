import os
from functools import lru_cache


class Settings:
    def __init__(self) -> None:
        self.openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))
        self.chunk_size: int = int(os.getenv("CHUNK_SIZE", "1200"))
        self.chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))
        self.frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")


@lru_cache
def get_settings() -> Settings:
    return Settings()
