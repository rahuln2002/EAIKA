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
        model: str = ("llama-3.3-70b-versatile"),
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
        )

        logger.info("Groq response received")

        return completion.choices[0].message.content

    @classmethod
    def stream_response(
        cls,
        prompt: str,
        model: str = ("llama-3.3-70b-versatile"),
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
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta

            if delta and delta.content:
                yield delta.content

        logger.info("Groq response streamed")
