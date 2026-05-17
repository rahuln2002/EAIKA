from mistralai.client import Mistral

from app.core.config.settings import (
    settings,
)

# =========================================================
# MISTRAL CLIENT
# =========================================================

client = Mistral(api_key=settings.MISTRAL_API_KEY)


class MistralService:
    """
    Mistral generation service.
    """

    MODEL_NAME = "mistral-small-latest"

    @classmethod
    def generate_response(
        cls,
        prompt: str,
    ) -> str:
        """
        Generate Mistral response.
        """

        response = client.chat.complete(
            model=cls.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content
