import json

from fastapi import HTTPException
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from app.config import get_settings
from app.services.observability_service import trace_event


def call_openai_json(
    messages: list[dict[str, str]],
    json_schema: dict,
    schema_name: str,
    model_type: type[BaseModel],
) -> BaseModel:
    settings = get_settings()

    if not settings.openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured. Add it to your environment and restart the backend.",
        )

    client = OpenAI(api_key=settings.openai_api_key)

    with trace_event("model_call", {"model": settings.openai_model, "schema": schema_name}):
        if hasattr(client, "responses"):
            response = client.responses.create(
                model=settings.openai_model,
                input=messages,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": schema_name,
                        "strict": True,
                        "schema": json_schema,
                    }
                },
            )
            raw_json = response.output_text
        else:
            response = client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema_name,
                        "strict": True,
                        "schema": json_schema,
                    },
                },
            )
            raw_json = response.choices[0].message.content or "{}"

    try:
        return model_type.model_validate(json.loads(raw_json))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The model returned an unexpected response format. Please try again.",
        ) from exc
