# AI Legal Document Reader

This is a final-version preview of the DocuLens learning project. It shows where the software can go after v1-v6: LangChain document loading, text splitting, retrieval-style document Q&A, multi-document comparison, and local observability events.

This app is for educational document analysis only. It is not legal advice and does not predict legal verdicts, guarantee outcomes, or tell users what legal action to take.

## Features

- React + Vite frontend
- FastAPI backend
- PDF upload and indexing
- LangChain `PyPDFLoader`
- LangChain `RecursiveCharacterTextSplitter`
- In-memory retrieval over document chunks
- OpenAI structured JSON outputs
- Pasted-text analysis
- Uploaded-document analysis with sources
- Document Q&A with retrieved source references
- Multi-document comparison
- Local observability events for indexing, retrieval, and model calls
- Docker Compose support
- Tests that do not call the real OpenAI API

## Architecture

```text
React frontend
  -> FastAPI API
  -> LangChain PDF loader
  -> LangChain text splitter
  -> in-memory document chunk store
  -> simple lexical retriever
  -> OpenAI structured JSON calls
  -> source references + observability events
```

## Local Setup

```bash
cp .env.example .env
```

Edit `.env` and set:

```text
OPENAI_API_KEY=your_api_key_here
```

## Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000 --env-file ../.env
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## Run Tests

```bash
cd backend
source .venv/bin/activate
pytest
```

## Run With Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

## API Overview

- `GET /health`
- `POST /api/documents`
- `GET /api/documents`
- `POST /api/analyze/text`
- `POST /api/analyze/document/{document_id}`
- `POST /api/questions`
- `POST /api/compare`
- `GET /api/observability/events`

## Safety Boundary

Every prompt instructs the model to:

- avoid legal advice
- avoid definitive legal conclusions
- avoid invented facts
- use only the provided document context
- say when information is missing or unclear
- frame outputs as possible outcomes, risks and ambiguities, and questions for a lawyer

## Current Limitation

The retrieval layer is intentionally simple and in-memory for learning. A production system would use durable document storage, embeddings, a vector database, authentication, background jobs, and a real observability platform such as Langfuse or LangSmith.
