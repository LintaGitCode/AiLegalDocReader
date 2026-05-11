import json

from fastapi import HTTPException
from openai import OpenAI
from pydantic import ValidationError

from app.config import get_settings
from app.schemas import ANALYSIS_JSON_SCHEMA, DocumentAnalysis
from app.services.prompt_service import build_analysis_prompt


def _extract_openai_json(client: OpenAI, model: str, messages: list[dict[str, str]]) -> str:
    if hasattr(client, "responses"):
        response = client.responses.create(
            model=model,
            input=messages,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "doculens_document_analysis",
                    "strict": True,
                    "schema": ANALYSIS_JSON_SCHEMA,
                }
            },
        )
        return response.output_text

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "doculens_document_analysis",
                "strict": True,
                "schema": ANALYSIS_JSON_SCHEMA,
            },
        },
    )
    return response.choices[0].message.content or "{}"


def validate_document_text(text: str) -> str:
    settings = get_settings()
    cleaned = text.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Please provide document text to analyze.")

    if len(cleaned) > settings.max_input_chars:
        raise HTTPException(
            status_code=413,
            detail=f"Document is too long for v1. Please keep input under {settings.max_input_chars} characters.",
        )

    return cleaned


def analyze_document_text(text: str) -> DocumentAnalysis:
    settings = get_settings()
    cleaned = validate_document_text(text)

    if not settings.openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured. Add it to your environment and restart the backend.",
        )

    # Future LangChain insertion point:
    # Replace this direct SDK call with a LangChain prompt template, model, and output parser.
    client = OpenAI(api_key=settings.openai_api_key)
    messages = build_analysis_prompt(cleaned)

    try:
        raw_json = _extract_openai_json(client, settings.openai_model, messages)
        return DocumentAnalysis.model_validate(json.loads(raw_json))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The model returned an unexpected response format. Please try again.",
        ) from exc
