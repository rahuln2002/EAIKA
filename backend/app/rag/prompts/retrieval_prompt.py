from app.rag.prompts.system_prompt import (
    SYSTEM_PROMPT,
)


def build_rag_prompt(
    query: str,
    context_chunks: list[str],
) -> str:
    """
    Construct RAG prompt with retrieved context.
    """

    context = "\n\n".join(context_chunks)

    prompt = f"""
{SYSTEM_PROMPT}

Retrieved Context:
{context}

User Question:
{query}

Instructions:
- Answer ONLY using retrieved context
- If answer is not found, say:
  "I could not find relevant information."
- Be accurate and concise

Answer:
"""

    return prompt
