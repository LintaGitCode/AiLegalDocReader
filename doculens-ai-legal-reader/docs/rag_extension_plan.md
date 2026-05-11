# RAG Extension Plan

RAG should be added after the app can reliably analyze one document with direct prompting and after text splitting is introduced.

## Chunk documents

v3 now splits documents into smaller chunks with LangChain `RecursiveCharacterTextSplitter`. Each chunk keeps page metadata and receives a `chunk_index`.

Current v3 chunk flow:

```text
PDF
  -> PyPDFLoader
  -> page Documents
  -> RecursiveCharacterTextSplitter
  -> chunk Documents
```

In v4, these chunk Documents become the records that will be embedded and retrieved.

## Create embeddings

Use an embeddings model to convert chunks into vectors. Store the original chunk text alongside each vector.

## Store vectors

Start with a local vector store for learning. Later, move to a managed vector database or AWS-native option.

## Retrieve relevant chunks

For each analysis task or user question, retrieve only the most relevant chunks instead of sending the entire document to the model.

## Generate grounded answers

Send retrieved chunks to the model and ask it to cite or reference source chunks. The prompt should still avoid legal advice and definitive legal conclusions.

## Source references

Return source references in the UI so users can see which document sections informed the analysis.
