import time

from fastapi import (
    WebSocket,
    WebSocketDisconnect,
)

from jose import jwt
from jose import JWTError

from sqlalchemy.orm import Session

from app.core.config.settings import (
    settings,
)

from app.db.session import SessionLocal

from app.services.chat.chat_service import (
    ChatService,
)

from app.services.analytics.analytics_service import (
    AnalyticsService,
)

from app.services.retrieval.retrieval_service import (
    RetrievalService,
)

from app.services.llm.provider_manager import (
    ProviderManager,
)

from app.rag.prompts.retrieval_prompt import (
    build_rag_prompt,
)

from app.websockets.connection_manager import (
    ConnectionManager,
)

# =====================================================
# WS MANAGER
# =====================================================

manager = ConnectionManager()


class WebSocketHandler:
    """
    Enterprise streaming WebSocket handler.
    """

    @staticmethod
    async def handle_chat(
        websocket: WebSocket,
        token: str,
        chat_id: int | None = None,
    ):
        """
        Handle conversational AI chat.
        """

        await manager.connect(websocket)

        db: Session = SessionLocal()

        try:
            # =================================================
            # AUTHENTICATE USER
            # =================================================

            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
            )

            user_id = int(payload.get("sub"))

            if not user_id:
                await websocket.close(code=4001)
                return

            # =================================================
            # CHAT SESSION
            # =================================================

            if chat_id:
                chat = ChatService.get_chat(
                    db=db,
                    chat_id=chat_id,
                    user_id=user_id,
                )

                if not chat:
                    await websocket.close(code=4004)
                    return

            else:
                chat = ChatService.create_chat(
                    db=db,
                    user_id=user_id,
                )

            await manager.send_chat_id(
                websocket,
                chat.id,
            )

            # =================================================
            # MAIN LOOP
            # =================================================

            retrieval_service = RetrievalService()

            while True:
                query = await websocket.receive_text()

                start_time = time.time()

                # =============================================
                # RETRIEVE CONTEXT
                # =============================================

                retrieved_chunks = retrieval_service.retrieve_context(
                    query=query,
                    db=db,
                    user_id=user_id,
                    top_k=5,
                )

                # =============================================
                # CONTEXT EXTRACTION
                # =============================================

                context_chunks = [chunk["content"] for chunk in retrieved_chunks]

                # =============================================
                # CONVERSATION HISTORY
                # =============================================

                conversation_history = ChatService.get_chat_history(
                    db=db,
                    chat_id=chat.id,
                )

                # =============================================
                # SAVE USER MESSAGE
                # =============================================

                ChatService.save_message(
                    db=db,
                    chat_id=chat.id,
                    role="user",
                    content=query,
                )

                # =============================================
                # BUILD PROMPT
                # =============================================

                prompt = build_rag_prompt(
                    query=query,
                    context_chunks=context_chunks,
                    conversation_history=(conversation_history),
                )

                # =============================================
                # STREAM RESPONSE
                # =============================================

                stream = ProviderManager.stream_response(
                    provider="groq",
                    prompt=prompt,
                )

                full_response = ""

                for token in stream:
                    full_response += token

                    await manager.send_token(
                        websocket,
                        token,
                    )

                # =============================================
                # SAVE ASSISTANT MESSAGE
                # =============================================

                ChatService.save_message(
                    db=db,
                    chat_id=chat.id,
                    role="assistant",
                    content=full_response,
                )

                # =============================================
                # ANALYTICS
                # =============================================

                response_time = time.time() - start_time

                AnalyticsService.log_analytics(
                    db=db,
                    user_id=user_id,
                    query=query,
                    response_time=response_time,
                    retrieved_chunks=len(retrieved_chunks),
                )

                # =============================================
                # SEND SOURCES
                # =============================================

                await manager.send_sources(
                    websocket,
                    retrieved_chunks,
                )

                # =============================================
                # END STREAM
                # =============================================

                await manager.send_end(
                    websocket,
                )

        except JWTError:
            await websocket.close(code=4001)

        except WebSocketDisconnect:
            manager.disconnect(websocket)

        except Exception as e:
            print(f"WebSocket Error: {e}")

            await websocket.close(code=1011)

        finally:
            db.close()
