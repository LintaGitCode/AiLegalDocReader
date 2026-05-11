# DocuLens AI Legal Document Reader

DocuLens is a beginner-friendly full-stack learning project for analyzing legal-style documents with the OpenAI API. Users can paste document text or upload a PDF and receive structured educational analysis.

## What the app does

- Accepts pasted legal-style document text.
- Accepts simple PDF uploads, loads them with LangChain, and splits them into chunks.
- Sends document text to OpenAI for structured JSON analysis.
- Displays document type, summary, parties, important dates, obligations, risks, possible outcomes, lawyer questions, confidence notes, and a disclaimer.

## What the app does not do

- It does not provide legal advice.
- It does not predict a legal verdict.
- It does not say who will win a dispute.
- It does not guarantee outcomes.
- It does not tell users whether they should sue, sign, or take legal action.

## Legal safety disclaimer

DocuLens provides educational document analysis only. It can help identify issues to review, risks and ambiguities, possible outcomes, and questions to ask a lawyer. It is not a substitute for advice from a qualified attorney.

## Architecture

```text
React + Vite frontend
  -> POST /api/analyze/text or /api/analyze/pdf
FastAPI backend
  -> LangChain PyPDFLoader loads PDF pages as Documents
  -> LangChain RecursiveCharacterTextSplitter splits pages into chunks
  -> prompt_service.py builds the safety-focused prompt
  -> analysis_service.py calls the OpenAI Responses API
  -> structured JSON is validated with Pydantic
Frontend
  -> displays the structured analysis sections
```

## Local setup

From this folder:

```bash
cp .env.example .env
```

Edit `.env` and set:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Environment variables

- `OPENAI_API_KEY`: Required for real analysis calls.
- `OPENAI_MODEL`: Model used by the backend. Defaults to `gpt-4o-mini`.
- `MAX_INPUT_CHARS`: Character limit for pasted or extracted text. Defaults to `20000`.
- `CHUNK_SIZE`: Target size for LangChain document chunks. Defaults to `1200`.
- `CHUNK_OVERLAP`: Overlap between neighboring chunks. Defaults to `150`.
- `FRONTEND_ORIGIN`: CORS origin for local frontend. Defaults to `http://localhost:5173`.
- `VITE_API_BASE_URL`: Frontend API target. Defaults to `http://localhost:8000`.

## Run the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000 --env-file ../.env
```

Visit:

```text
http://localhost:8000/health
```

## Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## Run tests

```bash
cd backend
source .venv/bin/activate
pytest
```

The tests do not call the real OpenAI API. The text analysis route test replaces the OpenAI-backed service with a mock function.

## Run with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Open the frontend at:

```text
http://localhost:5173
```

Backend runs at:

```text
http://localhost:8000
```

## Where OpenAI is used

OpenAI is called in `backend/app/services/analysis_service.py`. The app uses the OpenAI Python SDK and the Responses API with a JSON schema so the backend receives predictable structured output.

The safety-focused prompt lives in `backend/app/services/prompt_service.py`.

## How LangChain is used in v3

LangChain is used in the PDF pipeline through `PyPDFLoader` and `RecursiveCharacterTextSplitter`.

The app still sends joined document text to the existing OpenAI analysis service, but the joined text now comes from smaller LangChain chunks instead of whole PDF pages.

Current PDF flow:

```text
PDF upload
  -> PyPDFLoader
  -> page-level LangChain Document objects
  -> RecursiveCharacterTextSplitter
  -> chunk-level LangChain Document objects
  -> joined chunk text with page/chunk markers
  -> OpenAI structured analysis
```

This prepares the app for v4 RAG because chunks are the unit that will later be embedded, stored, retrieved, and cited.

Future versions can expand LangChain usage with:

- Prompt templates
- Model wrappers
- Chains
- Structured output parsers

See `docs/langchain_extension_plan.md`.

## How RAG will be added later

RAG will support longer documents by splitting text into chunks, embedding chunks, storing vectors, retrieving relevant passages, and generating grounded answers with source references.

See `docs/rag_extension_plan.md`.

## How AWS deployment will be added later

AWS deployment can use Docker images in ECR, ECS Fargate services behind an Application Load Balancer, S3 for uploaded PDFs, and Secrets Manager or SSM Parameter Store for the OpenAI API key.

See `docs/aws_deployment_plan.md`.

## How Langfuse observability will be added later

Langfuse can trace prompts, model calls, latency, token usage, retrieval quality, and user feedback once the core flow is stable.

See `docs/langfuse_observability_plan.md`.
