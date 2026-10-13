from groq import Groq

from app.core.config.settings import (
    settings,
)
from app.monitoring.logging import logger


class GroqService:
    """
    Groq LLM service.
    """

    client = Groq(api_key=settings.GROQ_API_KEY)

    @classmethod
    def generate_response(
        cls,
        prompt: str,
        model: str = ("openai/gpt-oss-120b"),
    ) -> str:
        """
        Generate normal response.
        """

        logger.info("Sending Groq request...")

        completion = cls.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stop=None,
        )

        logger.info("Groq response received")

        return completion.choices[0].message.content

    @classmethod
    def stream_response(
        cls,
        prompt: str,
        model: str = ("openai/gpt-oss-120b"),
    ):
        """
        Stream response tokens.
        """

        logger.info("Streaming Groq request...")
        stream = cls.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta

            if delta and delta.content:
                yield delta.content

        logger.info("Groq response streamed")
