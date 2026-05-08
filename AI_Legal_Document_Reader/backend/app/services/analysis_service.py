from fastapi import HTTPException

from app.config import get_settings
from app.schemas import (
    ANALYSIS_JSON_SCHEMA,
    COMPARISON_JSON_SCHEMA,
    QA_JSON_SCHEMA,
    ComparisonAnalysis,
    DocumentAnalysis,
    QuestionAnswer,
)
from app.services.document_service import source_reference_from_document
from app.services.openai_service import call_openai_json
from app.services.prompt_service import build_analysis_messages, build_comparison_messages, build_qa_messages
from app.services.retrieval_service import documents_to_context, retrieve_chunks


def validate_text(text: str) -> str:
    settings = get_settings()
    cleaned = text.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Please provide document text to analyze.")

    if len(cleaned) > settings.max_input_chars:
        raise HTTPException(
            status_code=413,
            detail=f"Document is too long. Please keep input under {settings.max_input_chars} characters.",
        )

    return cleaned


def analyze_text(text: str) -> DocumentAnalysis:
    cleaned = validate_text(text)
    result = call_openai_json(
        messages=build_analysis_messages(cleaned),
        json_schema=ANALYSIS_JSON_SCHEMA,
        schema_name="document_analysis",
        model_type=DocumentAnalysis,
    )
    result.source_references = []
    return result


def analyze_document(document_id: str) -> DocumentAnalysis:
    chunks = retrieve_chunks(
        [document_id],
        "document type summary parties important dates obligations risks ambiguities possible outcomes",
    )
    if not chunks:
        raise HTTPException(status_code=404, detail="Document not found. Upload a PDF first.")

    result = call_openai_json(
        messages=build_analysis_messages(documents_to_context(chunks)),
        json_schema=ANALYSIS_JSON_SCHEMA,
        schema_name="document_analysis",
        model_type=DocumentAnalysis,
    )
    result.source_references = [source_reference_from_document(chunk) for chunk in chunks]
    return result


def answer_question(document_id: str, question: str) -> QuestionAnswer:
    cleaned_question = validate_text(question)
    chunks = retrieve_chunks([document_id], cleaned_question)
    if not chunks:
        raise HTTPException(status_code=404, detail="Document not found. Upload a PDF first.")

    result = call_openai_json(
        messages=build_qa_messages(cleaned_question, documents_to_context(chunks)),
        json_schema=QA_JSON_SCHEMA,
        schema_name="document_question_answer",
        model_type=QuestionAnswer,
    )
    result.source_references = [source_reference_from_document(chunk) for chunk in chunks]
    return result


def compare_documents(document_ids: list[str]) -> ComparisonAnalysis:
    if len(document_ids) < 2:
        raise HTTPException(status_code=400, detail="Choose at least two documents to compare.")

    chunks = retrieve_chunks(
        document_ids,
        "compare obligations differences conflicts dates parties termination payment ambiguity",
    )
    if not chunks:
        raise HTTPException(status_code=404, detail="No uploaded documents found for comparison.")

    result = call_openai_json(
        messages=build_comparison_messages(documents_to_context(chunks)),
        json_schema=COMPARISON_JSON_SCHEMA,
        schema_name="document_comparison",
        model_type=ComparisonAnalysis,
    )
    result.source_references = [source_reference_from_document(chunk) for chunk in chunks]
    return result
