import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings


def load_pdf_documents_from_bytes(file_bytes: bytes) -> list[Document]:
    temp_file_path = ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_bytes)
            temp_file_path = temp_file.name

        loader = PyPDFLoader(temp_file_path)
        return loader.load()
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def split_documents_into_chunks(documents: list[Document]) -> list[Document]:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index

    return chunks


def extract_text_from_pdf(file_bytes: bytes) -> str:
    documents = load_pdf_documents_from_bytes(file_bytes)
    chunks = split_documents_into_chunks(documents)
    chunk_texts: list[str] = []

    for chunk in chunks:
        if chunk.page_content.strip():
            page = chunk.metadata.get("page", "unknown")
            chunk_index = chunk.metadata.get("chunk_index", "unknown")
            chunk_texts.append(
                f"[Page {page}, chunk {chunk_index}]\n{chunk.page_content.strip()}"
            )

    return "\n\n".join(chunk_texts).strip()
