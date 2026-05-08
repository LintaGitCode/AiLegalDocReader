import re
from collections import Counter

from langchain_core.documents import Document

from app.config import get_settings
from app.services.document_service import get_document_chunks
from app.services.observability_service import trace_event


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_'-]+", text.lower())
        if len(token) > 2
    }


def _score(query_tokens: set[str], document: Document) -> int:
    counts = Counter(re.findall(r"[a-zA-Z][a-zA-Z0-9_'-]+", document.page_content.lower()))
    return sum(counts[token] for token in query_tokens)


def retrieve_chunks(document_ids: list[str], query: str) -> list[Document]:
    query_tokens = _tokens(query)
    candidates: list[Document] = []

    for document_id in document_ids:
        candidates.extend(get_document_chunks(document_id))

    with trace_event(
        "retrieval",
        {"document_count": len(document_ids), "candidate_chunks": len(candidates)},
    ):
        ranked = sorted(candidates, key=lambda chunk: _score(query_tokens, chunk), reverse=True)

    return ranked[: get_settings().max_retrieved_chunks]


def documents_to_context(documents: list[Document]) -> str:
    sections: list[str] = []

    for document in documents:
        filename = document.metadata.get("filename", "Uploaded document")
        page = document.metadata.get("page", "unknown")
        chunk_index = document.metadata.get("chunk_index", "unknown")
        sections.append(
            f"[Source: {filename}, page {page}, chunk {chunk_index}]\n{document.page_content}"
        )

    return "\n\n".join(sections)
