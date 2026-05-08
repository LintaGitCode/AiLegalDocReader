import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf_documents_from_bytes(file_bytes: bytes, filename: str) -> list[Document]:
    temp_file_path = ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_bytes)
            temp_file_path = temp_file.name

        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()

        for document in documents:
            document.metadata["filename"] = filename

        return documents
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
