def build_summary_prompt(
    text: str,
) -> str:
    """
    Build summarization prompt.
    """

    prompt = f"""
You are an enterprise AI summarization assistant.

Summarize the following content clearly and accurately.

Requirements:
- Preserve important information
- Avoid hallucinations
- Be concise
- Use professional language

Content:
{text}

Summary:
"""

    return prompt


def build_reduce_prompt(
    summaries: list[str],
) -> str:
    """
    Build reduce summarization prompt.
    """

    combined = "\n\n".join(summaries)

    prompt = f"""
You are an enterprise AI summarizer.

Combine the following partial summaries into a single coherent executive summary.

Requirements:
- Remove redundancy
- Preserve key insights
- Keep clarity high
- Produce concise output

Partial Summaries:
{combined}

Final Executive Summary:
"""

    return prompt
