from app.services.llm.llama_service import (
    LlamaService,
)
from app.services.llm.mistral_service import (
    MistralService,
)
from app.services.llm.openai_service import (
    OpenAIService,
)


class ProviderManager:
    """
    Unified LLM provider manager.
    """

    PROVIDERS = {
        "openai": OpenAIService,
        "mistral": MistralService,
        "llama": LlamaService,
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
