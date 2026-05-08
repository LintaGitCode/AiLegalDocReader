# Observability

This project includes simple local observability events for learning.

Tracked event types:

- `pdf_index`
- `retrieval`
- `model_call`

The endpoint is:

```text
GET /api/observability/events
```

Future observability tools:

- Langfuse
- LangSmith
- OpenTelemetry-compatible traces

Future metrics:

- prompt versions
- retrieved chunks
- model latency
- token usage
- structured output failures
- user feedback
