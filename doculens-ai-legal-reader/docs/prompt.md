You are helping me build my first Codex-assisted AI engineering project.

Project name:
DocuLens AI Legal Document Reader

Goal:
Create a simple full-stack application that lets a user upload a PDF or paste legal-style document text and receive an AI-generated structured analysis.

This is a learning project to help me understand:
- OpenAI API usage
- prompt design
- structured model outputs
- PDF text extraction
- FastAPI backend design
- React frontend design
- how LangChain can be added later
- how RAG can be added later
- how AWS deployment can be added later

Important safety requirement:
This app must not claim to provide legal advice. It must not predict a definitive legal verdict. It should provide educational document analysis only.

Use safer language:
- "possible outcomes"
- "risks and ambiguities"
- "issues to review"
- "questions to ask a lawyer"

Avoid unsafe language:
- "legal verdict"
- "who will win"
- "guaranteed outcome"
- "you should sue"
- "you should sign"

Version 1 scope:
Keep the first version as simple as possible.

Build:
1. React + Vite frontend
2. FastAPI backend
3. PDF upload support
4. Paste-text support
5. PDF text extraction
6. OpenAI-powered structured analysis
7. Clear frontend display of the analysis
8. Local development instructions
9. Docker support if straightforward

Do not add yet:
- LangChain implementation
- RAG
- vector database
- agents
- Langfuse
- AWS deployment
- authentication
- production database

However, structure the code so LangChain and RAG can be added later.

Repository structure:
Create this structure:

doculens-ai-legal-reader/
  README.md
  .env.example
  .gitignore
  docker-compose.yml

  backend/
    Dockerfile
    requirements.txt
    app/
      main.py
      config.py
      schemas.py

      api/
        health.py
        analyze.py

      services/
        pdf_service.py
        analysis_service.py
        prompt_service.py

      tests/
        test_health.py
        test_text_analysis.py
        test_pdf_service.py

  frontend/
    Dockerfile
    package.json
    index.html
    src/
      main.jsx
      App.jsx
      api.js
      styles.css

  docs/
    roadmap.md
    langchain_extension_plan.md
    rag_extension_plan.md
    langfuse_observability_plan.md
    aws_deployment_plan.md

Backend requirements:
1. Use FastAPI.
2. Add these endpoints:
   - GET /health
   - POST /api/analyze/text
   - POST /api/analyze/pdf
3. POST /api/analyze/text should accept raw text.
4. POST /api/analyze/pdf should accept a PDF file upload.
5. Extract text from PDFs using a simple Python PDF library such as pypdf.
6. Send extracted text to OpenAI for structured analysis.
7. Read OPENAI_API_KEY from environment variables.
8. Read OPENAI_MODEL from environment variables.
9. Return structured JSON with this schema:
   - document_type
   - summary
   - parties
   - important_dates
   - key_obligations
   - risks_or_ambiguities
   - possible_outcomes
   - questions_for_lawyer
   - confidence_notes
   - disclaimer
10. Add validation for empty input.
11. Add friendly error handling for missing OPENAI_API_KEY.
12. Add a maximum character limit for v1 so very large PDFs do not break the app.
13. Add comments explaining where LangChain could later be inserted.

OpenAI requirements:
1. Use the OpenAI Python SDK.
2. Prefer the current OpenAI Responses API style if practical.
3. Ask the model to return structured JSON.
4. Keep the prompt in prompt_service.py.
5. The prompt must clearly say:
   - this is not legal advice
   - the model should not invent facts
   - the model should base the analysis only on the document text
   - the model should say when information is missing
   - the model should avoid definitive legal conclusions

Frontend requirements:
1. Use React + Vite.
2. The UI should have:
   - title: DocuLens AI Legal Document Reader
   - disclaimer banner
   - PDF upload input
   - paste-text area
   - Analyze button
   - loading state
   - error display
   - structured analysis display
3. Display sections:
   - Document Type
   - Summary
   - Parties
   - Important Dates
   - Key Obligations
   - Risks or Ambiguities
   - Possible Outcomes
   - Questions for a Lawyer
   - Confidence Notes
   - Disclaimer
4. Use plain CSS.
5. Keep the UI beginner-friendly.
6. Put API calls in src/api.js.

Testing requirements:
1. Add pytest tests for:
   - health endpoint
   - empty text validation
   - PDF text extraction
2. Tests should not call the real OpenAI API.
3. Mock the OpenAI call in text-analysis tests.
4. Include clear instructions for running tests.

Docker requirements:
1. Add a backend Dockerfile.
2. Add a frontend Dockerfile.
3. Add docker-compose.yml if practical.
4. docker-compose should run:
   - backend on port 8000
   - frontend on port 5173
5. Use .env support for OPENAI_API_KEY and OPENAI_MODEL.

Documentation requirements:
Update README.md with:
1. Project overview
2. What the app does
3. What the app does not do
4. Legal safety disclaimer
5. Architecture diagram in text form
6. Local setup
7. Environment variables
8. How to run backend
9. How to run frontend
10. How to run tests
11. How to run with Docker Compose
12. Explanation of where OpenAI is used
13. Explanation of how LangChain will be added later
14. Explanation of how RAG will be added later
15. Explanation of how AWS deployment will be added later
16. Explanation of how Langfuse observability will be added later

Create docs/langchain_extension_plan.md:
Explain how a future version will add LangChain for:
- PDF document loaders
- text splitting
- prompt templates
- chains
- output parsing

Create docs/rag_extension_plan.md:
Explain how a future version will add RAG:
- chunk documents
- create embeddings
- store vectors
- retrieve relevant chunks
- generate grounded answers with source references

Create docs/langfuse_observability_plan.md:
Explain how Langfuse will later be added to observe:
- prompts
- model calls
- latency
- token usage
- retrieval quality
- user feedback

Create docs/aws_deployment_plan.md:
Explain how the app will later be deployed using:
- Docker
- ECR
- ECS Fargate
- Application Load Balancer
- S3 for uploaded PDFs
- Secrets Manager or SSM Parameter Store for OpenAI API key

Acceptance criteria:
- I can run the backend locally.
- I can run the frontend locally.
- I can paste legal-style text and get structured analysis.
- I can upload a simple PDF and get structured analysis.
- The app clearly says it is not legal advice.
- The code is simple and beginner-friendly.
- Tests do not call the real OpenAI API.
- The project is structured so LangChain and RAG can be added later.

Work style:
Before making changes, briefly summarize your implementation plan.
Then create the files.
After implementation, tell me:
1. What you created.
2. How the document analysis flow works.
3. Where OpenAI is used.
4. Where LangChain will be added later.
5. How to run locally.
6. How to run tests.
7. How to run with Docker Compose.
8. The next 5 prompts I should give you.