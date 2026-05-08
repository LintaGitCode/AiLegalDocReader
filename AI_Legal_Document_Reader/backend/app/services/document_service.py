from uuid import uuid4

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings
from app.schemas import DocumentRecord, SourceReference
from app.services.observability_service import trace_event
from app.services.pdf_service import load_pdf_documents_from_bytes

_DOCUMENTS: dict[str, list[Document]] = {}
_RECORDS: dict[str, DocumentRecord] = {}


def _split_documents(documents: list[Document], document_id: str) -> list[Document]:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["document_id"] = document_id
        chunk.metadata["chunk_index"] = index

    return chunks


def index_pdf(file_bytes: bytes, filename: str) -> DocumentRecord:
    document_id = str(uuid4())

    with trace_event("pdf_index", {"filename": filename}):
        pages = load_pdf_documents_from_bytes(file_bytes, filename)
        chunks = _split_documents(pages, document_id)

    record = DocumentRecord(document_id=document_id, filename=filename, chunk_count=len(chunks))
    _DOCUMENTS[document_id] = chunks
    _RECORDS[document_id] = record
    return record


def list_documents() -> list[DocumentRecord]:
    return list(_RECORDS.values())


def get_document_chunks(document_id: str) -> list[Document]:
    return _DOCUMENTS.get(document_id, [])


def source_reference_from_document(document: Document) -> SourceReference:
    preview = " ".join(document.page_content.split())[:220]
    return SourceReference(
        document_id=str(document.metadata.get("document_id", "")),
        filename=str(document.metadata.get("filename", "Uploaded document")),
        page=document.metadata.get("page"),
        chunk_index=int(document.metadata.get("chunk_index", 0)),
        preview=preview,
    )


def clear_document_store() -> None:
    _DOCUMENTS.clear()
    _RECORDS.clear()
