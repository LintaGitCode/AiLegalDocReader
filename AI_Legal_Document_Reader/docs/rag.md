# RAG Design

This preview uses a lightweight in-memory retrieval layer.

Current flow:

```text
PDF upload
  -> PyPDFLoader
  -> LangChain Document pages
  -> RecursiveCharacterTextSplitter
  -> chunks with metadata
  -> lexical retrieval
  -> OpenAI answer using retrieved context
```

Future production flow:

```text
chunks
  -> embeddings
  -> vector database
  -> semantic retriever
  -> grounded generation
  -> citations
```

The source references in the API response already prepare the UI for later vector-search citations.
