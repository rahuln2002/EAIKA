import ollama


class LlamaService:
    """
    Local Llama inference service.
    """

    MODEL_NAME = "llama3"

    @classmethod
    def generate_response(
        cls,
        prompt: str,
    ) -> str:
        """
        Generate local Llama response.
        """

        response = ollama.chat(
            model=cls.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]
