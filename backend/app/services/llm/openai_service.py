from openai import OpenAI

from app.core.config.settings import (
    settings,
)

# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:
    """
    OpenAI generation service.
    """

    MODEL_NAME = "gpt-4o-mini"

    @classmethod
    def generate_response(
        cls,
        prompt: str,
    ) -> str:
        """
        Generate OpenAI response.
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
