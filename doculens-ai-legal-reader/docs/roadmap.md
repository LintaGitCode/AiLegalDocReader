# Roadmap

| Stage | Focus |
| --- | --- |
| v1 | Prompting, structured outputs, OpenAI API |
| v2 | LangChain document loaders for PDFs |
| v3 | Text splitting for long documents |
| v4 | RAG with embeddings and vector search |
| v5 | Multi-document comparison |
| v6 | Langfuse observability |
| v7 | AWS storage, ECS deployment, and managed vector search |

## v1 acceptance goals

- Run the backend locally.
- Run the frontend locally.
- Paste legal-style text and receive structured analysis.
- Upload a simple PDF and receive structured analysis.
- Clearly state that this is not legal advice.
- Keep tests offline from the real OpenAI API.

## v2 acceptance goals

- PDF extraction uses LangChain `PyPDFLoader`.
- The existing PDF upload endpoint keeps the same request and response shape.
- Tests confirm PDF text extraction still works.
- Tests confirm LangChain document metadata is available for later RAG/source references.

## v3 acceptance goals

- PDF pages are split with LangChain `RecursiveCharacterTextSplitter`.
- Chunk size and overlap are configurable with environment variables.
- Chunks preserve original page metadata.
- Chunks receive a `chunk_index` for later RAG/source references.
- The existing PDF upload endpoint keeps the same request and response shape.
