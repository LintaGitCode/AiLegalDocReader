from fastapi import APIRouter

from app.schemas import (
    CompareRequest,
    ComparisonAnalysis,
    DocumentAnalysis,
    QuestionAnswer,
    QuestionRequest,
    TextAnalysisRequest,
)
from app.services.analysis_service import analyze_document, analyze_text, answer_question, compare_documents

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze/text", response_model=DocumentAnalysis)
def analyze_pasted_text(request: TextAnalysisRequest) -> DocumentAnalysis:
    return analyze_text(request.text)


@router.post("/analyze/document/{document_id}", response_model=DocumentAnalysis)
def analyze_uploaded_document(document_id: str) -> DocumentAnalysis:
    return analyze_document(document_id)


@router.post("/questions", response_model=QuestionAnswer)
def ask_document_question(request: QuestionRequest) -> QuestionAnswer:
    return answer_question(request.document_id, request.question)


@router.post("/compare", response_model=ComparisonAnalysis)
def compare_uploaded_documents(request: CompareRequest) -> ComparisonAnalysis:
    return compare_documents(request.document_ids)
