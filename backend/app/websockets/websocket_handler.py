from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.rag.prompts.retrieval_prompt import (
    build_rag_prompt,
)
from app.services.llm.provider_manager import (
    ProviderManager,
)
from app.websockets.connection_manager import (
    ConnectionManager,
)

manager = ConnectionManager()


class WebSocketHandler:
    """
    Production streaming WebSocket handler.
    """

    @staticmethod
    async def handle_chat(
        websocket: WebSocket,
    ):
        """
        Handle streaming AI chat.
        """

        await manager.connect(websocket)

        try:
            while True:
                query = await websocket.receive_text()

                # =========================================
                # TEMP CONTEXT
                # =========================================

                context_chunks = [
                    "Retrieval-Augmented Generation improves factual AI systems.",
                    "Embeddings enable semantic search.",
                ]

                # =========================================
                # BUILD PROMPT
                # =========================================

                prompt = build_rag_prompt(
                    query=query,
                    context_chunks=context_chunks,
                    conversation_history=[],
                )

                # =========================================
                # STREAM TOKENS
                # =========================================

                stream = ProviderManager.stream_response(
                    provider="openai",
                    prompt=prompt,
                )

                for token in stream:
                    await manager.send_message(
                        websocket,
                        token,
                    )

                # =========================================
                # END MARKER
                # =========================================

                await manager.send_message(websocket, "[END]")

        except WebSocketDisconnect:
            manager.disconnect(websocket)
