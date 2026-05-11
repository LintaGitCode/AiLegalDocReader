from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., description="Legal-style document text to analyze.")


class DocumentAnalysis(BaseModel):
    document_type: str
    summary: str
    parties: list[str]
    important_dates: list[str]
    key_obligations: list[str]
    risks_or_ambiguities: list[str]
    possible_outcomes: list[str]
    questions_for_lawyer: list[str]
    confidence_notes: str
    disclaimer: str


ANALYSIS_JSON_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "document_type": {"type": "string"},
        "summary": {"type": "string"},
        "parties": {"type": "array", "items": {"type": "string"}},
        "important_dates": {"type": "array", "items": {"type": "string"}},
        "key_obligations": {"type": "array", "items": {"type": "string"}},
        "risks_or_ambiguities": {"type": "array", "items": {"type": "string"}},
        "possible_outcomes": {"type": "array", "items": {"type": "string"}},
        "questions_for_lawyer": {"type": "array", "items": {"type": "string"}},
        "confidence_notes": {"type": "string"},
        "disclaimer": {"type": "string"},
    },
    "required": [
        "document_type",
        "summary",
        "parties",
        "important_dates",
        "key_obligations",
        "risks_or_ambiguities",
        "possible_outcomes",
        "questions_for_lawyer",
        "confidence_notes",
        "disclaimer",
    ],
}
