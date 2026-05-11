from io import BytesIO

from reportlab.pdfgen import canvas

from app.services.pdf_service import (
    extract_text_from_pdf,
    load_pdf_documents_from_bytes,
    split_documents_into_chunks,
)


def make_test_pdf(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(72, 720, text)
    pdf.save()
    return buffer.getvalue()


def test_extract_text_from_pdf() -> None:
    pdf_bytes = make_test_pdf("Sample lease agreement text")

    extracted_text = extract_text_from_pdf(pdf_bytes)

    assert "Sample lease agreement text" in extracted_text
    assert "[Page 0, chunk 0]" in extracted_text


def test_load_pdf_documents_from_bytes_preserves_page_metadata() -> None:
    pdf_bytes = make_test_pdf("Metadata test text")

    documents = load_pdf_documents_from_bytes(pdf_bytes)

    assert len(documents) == 1
    assert "Metadata test text" in documents[0].page_content
    assert documents[0].metadata["page"] == 0


def test_split_documents_into_chunks_preserves_metadata(monkeypatch) -> None:
    monkeypatch.setenv("CHUNK_SIZE", "50")
    monkeypatch.setenv("CHUNK_OVERLAP", "10")

    from app.config import get_settings

    get_settings.cache_clear()
    pdf_bytes = make_test_pdf(
        "This lease contains rent terms, notice terms, termination terms, and renewal terms."
    )
    documents = load_pdf_documents_from_bytes(pdf_bytes)

    chunks = split_documents_into_chunks(documents)

    assert len(chunks) > 1
    assert chunks[0].metadata["page"] == 0
    assert chunks[0].metadata["chunk_index"] == 0

    get_settings.cache_clear()
