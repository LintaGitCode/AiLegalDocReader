# LangChain Extension Plan

LangChain v2 added PDF document loading. LangChain v3 adds text splitting while preserving the same API shape from earlier versions.

## PDF document loaders

The backend now routes PDF extraction through `PyPDFLoader` from `langchain_community.document_loaders`. This keeps page content and page metadata available for future source references.

Current flow:

```text
uploaded PDF bytes
  -> temporary PDF file
  -> PyPDFLoader.load()
  -> page-level LangChain Document objects
  -> RecursiveCharacterTextSplitter
  -> chunk-level LangChain Document objects
  -> joined chunk text for the existing analysis endpoint
```

The public backend function remains `extract_text_from_pdf(...)`, so the API route does not need to know whether extraction uses raw `pypdf` or LangChain.

## Text splitting

The backend now uses `RecursiveCharacterTextSplitter` from `langchain_text_splitters`.

Default settings:

```text
CHUNK_SIZE=1200
CHUNK_OVERLAP=150
```

Each chunk keeps the original page metadata and receives a `chunk_index`. The final text sent to OpenAI includes lightweight page/chunk markers:

```text
[Page 0, chunk 0]
...
```

This prepares the project for RAG because v4 can embed and retrieve chunks instead of entire pages or entire documents.

## Prompt templates

Move the current prompt into a LangChain prompt template. Keep the same safety rules:

- Not legal advice
- No invented facts
- Document-only analysis
- Missing information should be identified
- No definitive legal conclusions

## Chains

Create a simple analysis chain:

```text
document text -> prompt template -> model -> structured parser
```

Later, this can become a retrieval chain for RAG.

## Output parsing

Use a LangChain structured output parser or Pydantic parser to keep the same response schema currently defined in `backend/app/schemas.py`.
