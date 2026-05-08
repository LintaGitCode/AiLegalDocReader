from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., description="Legal-style document text to analyze.")


class QuestionRequest(BaseModel):
    document_id: str
    question: str


class CompareRequest(BaseModel):
    document_ids: list[str] = Field(..., min_length=2)


class SourceReference(BaseModel):
    document_id: str
    filename: str
    page: int | None = None
    chunk_index: int
    preview: str


class DocumentRecord(BaseModel):
    document_id: str
    filename: str
    chunk_count: int


class DocumentAnalysis(BaseModel):
    document_type: str
    summary: str
    parties: list[str]
    important_dates: list[str]
    key_obligations: list[str]
    risks_or_ambiguities: list[str]
    possible_outcomes: list[str]
    questions_for_lawyer: list[str]
    source_references: list[SourceReference]
    confidence_notes: str
    disclaimer: str


class QuestionAnswer(BaseModel):
    answer: str
    issues_to_review: list[str]
    source_references: list[SourceReference]
    disclaimer: str


class ComparisonAnalysis(BaseModel):
    summary: str
    shared_themes: list[str]
    differences: list[str]
    conflicting_or_unclear_terms: list[str]
    questions_for_lawyer: list[str]
    source_references: list[SourceReference]
    disclaimer: str


class ObservabilityEvent(BaseModel):
    event_type: str
    duration_ms: float | None = None
    metadata: dict[str, str | int | float | bool | None]


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


QA_JSON_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "answer": {"type": "string"},
        "issues_to_review": {"type": "array", "items": {"type": "string"}},
        "disclaimer": {"type": "string"},
    },
    "required": ["answer", "issues_to_review", "disclaimer"],
}


COMPARISON_JSON_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "summary": {"type": "string"},
        "shared_themes": {"type": "array", "items": {"type": "string"}},
        "differences": {"type": "array", "items": {"type": "string"}},
        "conflicting_or_unclear_terms": {"type": "array", "items": {"type": "string"}},
        "questions_for_lawyer": {"type": "array", "items": {"type": "string"}},
        "disclaimer": {"type": "string"},
    },
    "required": [
        "summary",
        "shared_themes",
        "differences",
        "conflicting_or_unclear_terms",
        "questions_for_lawyer",
        "disclaimer",
    ],
}
