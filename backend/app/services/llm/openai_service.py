from collections.abc import Generator

from openai import OpenAI

from app.core.config.settings import (
    settings,
)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:
    """
    OpenAI LLM service.
    """

    MODEL_NAME = "gpt-4o-mini"

    @classmethod
    def generate_response(
        cls,
        prompt: str,
    ) -> str:
        """
        Standard response generation.
        """

        response = client.chat.completions.create(
            model=cls.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    @classmethod
    def stream_response(
        cls,
        prompt: str,
    ) -> Generator[str, None, None]:
        """
        Stream token responses.
        """

        stream = client.chat.completions.create(
            model=cls.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content

            if delta:
                yield delta
