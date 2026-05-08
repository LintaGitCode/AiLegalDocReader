from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import DocumentRecord
from app.services.document_service import index_pdf, list_documents

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("", response_model=DocumentRecord)
async def upload_document(file: UploadFile = File(...)) -> DocumentRecord:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    file_bytes = await file.read()
    return index_pdf(file_bytes, file.filename or "uploaded.pdf")


@router.get("", response_model=list[DocumentRecord])
def get_documents() -> list[DocumentRecord]:
    return list_documents()
