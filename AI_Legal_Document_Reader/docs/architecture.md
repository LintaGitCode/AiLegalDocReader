# Architecture

```text
Frontend
  App.jsx
  api.js

Backend
  api/
    documents.py
    analyze.py
    observability.py

  services/
    pdf_service.py
    document_service.py
    retrieval_service.py
    analysis_service.py
    openai_service.py
    observability_service.py
```

FastAPI owns HTTP. LangChain owns document loading and splitting. The retrieval service finds relevant chunks. The OpenAI service handles structured JSON model calls. Observability records local events.
