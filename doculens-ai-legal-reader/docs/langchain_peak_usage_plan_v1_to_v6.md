# LangChain Peak Usage Plan: v1 to v6

This plan explains how DocuLens can grow from a simple OpenAI-powered document reader into a more complete LangChain-based legal-style document analysis system.

The safety rule stays the same in every version: DocuLens provides educational document analysis only. It must not provide legal advice, predict a legal verdict, guarantee outcomes, or tell users what legal action to take.

## Peak LangChain Vision

At maximum usage, LangChain becomes the orchestration layer for:

- PDF loading
- text splitting
- document metadata
- prompt templates
- model calls
- structured output parsing
- retrieval
- source citations
- multi-document comparison
- tracing and observability hooks

The backend would move from this:

```text
FastAPI
  -> extract PDF text
  -> build prompt manually
  -> call OpenAI directly
  -> parse JSON
```

To this:

```text
FastAPI
  -> LangChain document loaders
  -> LangChain text splitters
  -> LangChain embeddings
  -> LangChain vector store retriever
  -> LangChain prompt templates
  -> LangChain model wrapper
  -> LangChain structured output parser
  -> LangChain runnable chains
  -> tracing and observability
```

FastAPI remains the HTTP layer. LangChain becomes the document intelligence layer.

## v1: Prompting, Structured Outputs, OpenAI API

Goal: Build the simplest useful version.

What v1 does:

- Accept pasted text.
- Accept PDF upload.
- Extract PDF text.
- Send text to OpenAI.
- Ask OpenAI for structured JSON.
- Display structured sections in React.

LangChain usage:

- None.

Why this matters:

- v1 teaches the core request flow.
- It keeps the app understandable before adding orchestration tools.
- It establishes the response schema that later versions should preserve.

Main flow:

```text
User input
  -> FastAPI endpoint
  -> PDF extraction if needed
  -> prompt_service.py
  -> OpenAI API
  -> Pydantic validation
  -> React display
```

## v2: LangChain PDF Document Loaders

Goal: Introduce LangChain without changing the user experience.

What v2 adds:

- Use LangChain `PyPDFLoader`.
- Convert PDFs into LangChain `Document` objects.
- Preserve page metadata for future source references.
- Keep the same `/api/analyze/pdf` endpoint.

LangChain usage:

```text
PDF bytes
  -> temporary PDF file
  -> PyPDFLoader
  -> LangChain Document objects
  -> joined page_content
  -> existing analysis flow
```

Why this matters:

- LangChain `Document` objects contain both text and metadata.
- Metadata such as page number becomes important for RAG and citations.
- The rest of the app does not need to know how PDF loading works.

Future value:

```text
Document(page_content="...", metadata={"page": 3, "source": "lease.pdf"})
```

## v3: Text Splitting for Long Documents

Goal: Handle longer documents more safely and prepare for RAG.

What v3 adds:

- LangChain text splitters.
- Chunk large documents into smaller pieces.
- Keep chunk metadata.
- Avoid sending very large documents as one giant prompt.

Possible LangChain tool:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
)
```

Main flow:

```text
PDF
  -> PyPDFLoader
  -> Document objects
  -> text splitter
  -> smaller Document chunks
```

Why this matters:

- Long legal-style documents can exceed model limits.
- Splitting prepares the app for embeddings and retrieval.
- Chunk overlap helps preserve context between sections.

Example chunk metadata:

```json
{
  "source": "uploaded.pdf",
  "page": 2,
  "chunk_index": 5
}
```

## v4: RAG with Embeddings and Vector Search

Goal: Move from whole-document prompting to grounded retrieval.

What v4 adds:

- Embeddings for document chunks.
- Vector store for searchable document memory.
- Retriever to find relevant chunks.
- RAG prompt that answers using retrieved source text.
- Source references in responses.

Main flow:

```text
PDF
  -> load pages
  -> split into chunks
  -> create embeddings
  -> store vectors
  -> retrieve relevant chunks
  -> generate grounded answer
  -> return answer with sources
```

Questions RAG can support:

- What are the termination clauses?
- What payment duties are mentioned?
- What risks or ambiguities should be reviewed?
- Which dates matter?

User-facing improvement:

```text
Key Obligation:
Tenant must pay rent by the 1st of each month.

Source:
Page 2
```

Why this matters:

- The model does not need the entire document every time.
- Answers can be grounded in specific retrieved text.
- This is a major step from basic summary to document intelligence.

## v5: Multi-Document Comparison

Goal: Analyze relationships between multiple documents.

What v5 adds:

- Upload and index multiple PDFs.
- Compare document versions.
- Find conflicting obligations.
- Identify missing or changed clauses.
- Group analysis by document.

Example document set:

```text
lease_v1.pdf
lease_v2.pdf
addendum.pdf
notice.pdf
```

Possible features:

- Compare two contract versions.
- Summarize what changed.
- Identify conflicting dates or duties.
- Show which document each issue came from.

LangChain role:

- Load each document.
- Split each document.
- Store chunks with document-level metadata.
- Retrieve across one or many documents.
- Run comparison chains.

Main flow:

```text
Multiple PDFs
  -> loaders
  -> splitters
  -> vector store
  -> comparison retriever
  -> comparison chain
  -> structured comparison output
```

## v6: Observability and Evaluation

Goal: Understand how the AI system behaves in real use.

What v6 adds:

- Prompt tracing.
- Model call tracing.
- Latency tracking.
- Token usage tracking.
- Retrieval quality review.
- User feedback collection.
- Structured-output failure tracking.

Tools to consider:

- LangSmith
- Langfuse
- OpenTelemetry-style logs

What to observe:

- Which prompt version was used?
- Which chunks were retrieved?
- Did the retrieved chunks support the final answer?
- How long did retrieval take?
- How long did the model call take?
- How many tokens were used?
- Did JSON parsing fail?
- Did users rate the answer as helpful?

Why this matters:

- RAG systems can fail silently if retrieval is weak.
- Prompt changes need to be compared over time.
- Token and latency costs become important as usage grows.
- Feedback helps improve prompts, retrieval, and UI.

## Possible Advanced Backend Structure

As LangChain usage grows, the backend can move toward this structure:

```text
backend/app/
  api/
    analyze.py
    documents.py
    questions.py

  chains/
    document_analysis_chain.py
    rag_question_chain.py
    comparison_chain.py

  loaders/
    pdf_loader.py

  splitters/
    document_splitter.py

  retrievers/
    vector_retriever.py

  prompts/
    analysis_prompt.py
    rag_prompt.py
    comparison_prompt.py

  parsers/
    analysis_parser.py

  stores/
    vector_store.py
    document_store.py

  services/
    document_service.py
    analysis_service.py
```

## Recommended Learning Path

Build this gradually:

```text
v1: Direct OpenAI API and structured outputs
v2: LangChain PDF loader
v3: LangChain text splitter
v4: LangChain retriever and vector store
v5: Multi-document chains
v6: Tracing, evaluation, and feedback
```

Do not make LangChain control everything immediately. Each version should teach one new concept while keeping the app usable.
