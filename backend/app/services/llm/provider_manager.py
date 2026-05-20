from app.services.llm.groq_service import (
    GroqService,
)


class ProviderManager:
    """
    Unified LLM provider manager.
    """

    PROVIDERS = {
        "groq": GroqService,
    }

    @classmethod
    def generate_response(
        cls,
        provider: str,
        prompt: str,
    ) -> str:
        """
        Route generation request.
        """

        provider_service = cls.PROVIDERS.get(provider)

        if not provider_service:
            raise ValueError(f"Unsupported provider: {provider}")

        return provider_service.generate_response(prompt)

    @classmethod
    def stream_response(
        cls,
        provider: str,
        prompt: str,
    ):
        """
        Stream provider response.
        """

        provider_service = cls.PROVIDERS.get(provider)

        if not provider_service:
            raise ValueError(f"Unsupported provider: {provider}")

        return provider_service.stream_response(prompt)
