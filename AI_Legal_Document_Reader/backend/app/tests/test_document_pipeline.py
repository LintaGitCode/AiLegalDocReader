from io import BytesIO

from reportlab.pdfgen import canvas

from app.services.document_service import clear_document_store, get_document_chunks, index_pdf
from app.services.retrieval_service import retrieve_chunks


def make_pdf(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(72, 720, text)
    pdf.save()
    return buffer.getvalue()


def test_index_pdf_creates_langchain_chunks_with_metadata() -> None:
    clear_document_store()
    record = index_pdf(make_pdf("Lease requires rent payment on the first day."), "lease.pdf")
    chunks = get_document_chunks(record.document_id)

    assert record.filename == "lease.pdf"
    assert record.chunk_count >= 1
    assert chunks[0].metadata["document_id"] == record.document_id
    assert chunks[0].metadata["filename"] == "lease.pdf"
    assert "Lease requires rent payment" in chunks[0].page_content


def test_retrieve_chunks_returns_relevant_chunk() -> None:
    clear_document_store()
    record = index_pdf(make_pdf("The tenant must pay monthly rent before the fifth day."), "lease.pdf")

    chunks = retrieve_chunks([record.document_id], "rent payment")

    assert len(chunks) >= 1
    assert "rent" in chunks[0].page_content.lower()
