from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import DocumentAnalysis, TextAnalysisRequest
from app.services.analysis_service import analyze_document_text
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(prefix="/api/analyze", tags=["analysis"])


@router.post("/text", response_model=DocumentAnalysis)
def analyze_text(request: TextAnalysisRequest) -> DocumentAnalysis:
    return analyze_document_text(request.text)


@router.post("/pdf", response_model=DocumentAnalysis)
async def analyze_pdf(file: UploadFile = File(...)) -> DocumentAnalysis:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)
    return analyze_document_text(extracted_text)
