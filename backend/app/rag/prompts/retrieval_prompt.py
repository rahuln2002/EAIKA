from app.rag.prompts.system_prompt import (
    SYSTEM_PROMPT,
)


def build_rag_prompt(
    query: str,
    context_chunks: list[dict],
    conversation_history: list,
) -> str:
    """
    Build conversational RAG prompt.
    """

    context = "\n\n".join(
        chunk.get(
            "content",
            "",
        )
        for chunk in context_chunks
    )

    history = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in conversation_history
    )

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{history}

Retrieved Context:
{context}

Current User Question:
{query}

Instructions:
- Use conversation history for continuity
- Use retrieved context for factual grounding
- If information is unavailable, say so
- Be concise and accurate

Answer:
"""

    return prompt
