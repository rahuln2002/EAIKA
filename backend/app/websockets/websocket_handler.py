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
from app.db.session import SessionLocal
from app.services.retrieval.retrieval_service import RetrievalService

from jose import jwt
from jose import JWTError

from app.core.config.settings import (
    settings,
)

manager = ConnectionManager()


class WebSocketHandler:
    """
    Production streaming WebSocket handler.
    """

    @staticmethod
    async def handle_chat(
        websocket: WebSocket,
        token: str,
    ):
        """
        Handle streaming AI chat.
        """

        print("\nWEBSOCKET HANDLER RUNNING\n")
        await manager.connect(websocket)

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
            )

            user_id = int(payload.get("sub"))
            print(f"\nAUTH USER ID: {user_id}\n")
            if not user_id:
                await websocket.close(code=4001)
                return

        except JWTError:
            await websocket.close(code=4001)

            return

        try:
            while True:
                query = await websocket.receive_text()

                # =========================================
                # Database Session
                # =========================================

                db = SessionLocal()

                # =========================================
                # Retrieve CONTEXT
                # =========================================

                retrieval_service = RetrievalService()

                retrieved_chunks = retrieval_service.retrieve_context(
                    query=query,
                    db=db,
                    user_id=user_id,
                    top_k=5,
                )

                print("Retrieved Chunks:")
                print(retrieved_chunks)
                print("===============================")

                # =========================================
                # Extracted Content
                # =========================================

                context_chunks = [chunk["content"] for chunk in retrieved_chunks]

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
                    provider="groq",
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
