SAFETY_RULES = """
Safety rules:
- This is educational document analysis only, not legal advice.
- Base the answer only on the provided document context.
- Do not invent facts, dates, parties, duties, or legal conclusions.
- Say when information is missing, unclear, or not present in the context.
- Avoid definitive legal conclusions.
- Do not tell the user to sue, sign, refuse to sign, or take legal action.
- Use safer language such as possible outcomes, risks and ambiguities, issues to review, and questions to ask a lawyer.
""".strip()


def build_analysis_messages(context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": f"You are DocuLens AI Legal Document Reader.\n\n{SAFETY_RULES}",
        },
        {
            "role": "user",
            "content": f"Analyze this document context and return structured JSON.\n\nContext:\n{context}",
        },
    ]


def build_qa_messages(question: str, context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": f"You answer questions about legal-style documents.\n\n{SAFETY_RULES}",
        },
        {
            "role": "user",
            "content": f"Question:\n{question}\n\nRetrieved document context:\n{context}",
        },
    ]


def build_comparison_messages(context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": f"You compare legal-style documents for educational review.\n\n{SAFETY_RULES}",
        },
        {
            "role": "user",
            "content": f"Compare these retrieved document excerpts and return structured JSON.\n\nContext:\n{context}",
        },
    ]
