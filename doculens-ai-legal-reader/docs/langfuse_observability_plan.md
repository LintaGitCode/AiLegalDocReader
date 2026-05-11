# Langfuse Observability Plan

Langfuse should be added after the core app and RAG flow are stable. The goal is to understand how prompts, retrieval, and model calls behave in real use.

## Prompts

Track prompt versions so changes can be compared over time. This is especially useful for safety wording and structured output reliability.

## Model calls

Record model name, inputs, outputs, and errors for analysis calls. Sensitive document text should be handled carefully and redacted where appropriate.

## Latency

Measure total request time and model response time. This helps identify whether delays come from PDF extraction, retrieval, or generation.

## Token usage

Track token usage and cost trends by request type, document size, and model.

## Retrieval quality

Once RAG exists, trace retrieved chunks and compare them with the final answer. This helps detect weak retrieval or missing source context.

## User feedback

Add simple thumbs-up/thumbs-down feedback in the UI and send that feedback to Langfuse for later review.
