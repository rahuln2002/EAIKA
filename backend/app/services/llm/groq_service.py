from groq import Groq

from app.core.config.settings import (
    settings,
)


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
