import time
import traceback

from fastapi import (
    WebSocket,
    WebSocketDisconnect,
)

from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError

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

from app.monitoring.logging import (
    logger,
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

            if not token:
                await websocket.close(
                    code=4003,
                    reason="Unauthorized",
                )
                return

            try:
                payload = jwt.decode(
                    token,
                    settings.JWT_SECRET_KEY,
                    algorithms=["HS256"],
                )

            except ExpiredSignatureError:
                await websocket.close(
                    code=4002,
                    reason="Token expired",
                )
                return

            except JWTError:
                await websocket.close(
                    code=4001,
                    reason="Invalid token",
                )
                return

            sub = payload.get("sub")

            if not sub:
                await websocket.close(
                    code=4003,
                    reason="Unauthorized",
                )
                return

            try:
                user_id = int(sub)
            except (TypeError, ValueError):
                await websocket.close(
                    code=4003,
                    reason="Unauthorized",
                )
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
                    await websocket.close(
                        code=4004,
                        reason="Chat not found",
                    )
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

                retrieval_start = time.perf_counter()

                retrieved_chunks = retrieval_service.retrieve_context(
                    query=query,
                    db=db,
                    user_id=user_id,
                    top_k=5,
                )

                retrieval_time = time.perf_counter() - retrieval_start

                # =============================================
                # CONVERSATION HISTORY
                # =============================================

                history_start = time.perf_counter()

                conversation_history = ChatService.get_chat_history(
                    db=db,
                    chat_id=chat.id,
                )

                history_time = time.perf_counter() - history_start

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
                    context_chunks=retrieved_chunks,
                    conversation_history=(conversation_history),
                )

                # =============================================
                # STREAM RESPONSE
                # =============================================

                llm_start = time.perf_counter()

                stream = ProviderManager.stream_response(
                    provider="groq",
                    prompt=prompt,
                )

                full_response = ""

                buffer = ""

                for text in stream:
                    full_response += text

                    buffer += text

                    # =========================================
                    # STREAM BUFFER
                    # =========================================

                    if len(buffer) >= 20:
                        await manager.send_token(
                            websocket,
                            buffer,
                        )

                        buffer = ""

                # =============================================
                # SEND REMAINING BUFFER
                # =============================================

                if buffer:
                    await manager.send_token(
                        websocket,
                        buffer,
                    )

                llm_time = time.perf_counter() - llm_start

                evaluation = AnalyticsService.evaluate_response(
                    query=query,
                    answer=full_response,
                    retrieved_context=[chunk["content"] for chunk in retrieved_chunks],
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

                await manager.send_evaluation(
                    websocket,
                    evaluation,
                )

                # =============================================
                # END STREAM
                # =============================================

                await manager.send_end(
                    websocket,
                )

                # =============================================
                # ANALYTICS
                # =============================================

                total_response_time = time.time() - start_time

                try:
                    AnalyticsService.log_analytics(
                        db=db,
                        user_id=user_id,
                        query=query,
                        total_response_time=total_response_time,
                        retrieval_latency=retrieval_time,
                        history_latency=history_time,
                        llm_latency=llm_time,
                        retrieved_chunks=len(retrieved_chunks),
                    )
                except Exception as e:
                    logger.warning(f"Failed to log analytics: {e}")

        except WebSocketDisconnect:
            pass

        except Exception as e:
            traceback.print_exc()

            logger.warning(f"WebSocket Error: {e}")

            try:
                if websocket.client_state.name == "CONNECTED":
                    await websocket.send_json(
                        {
                            "type": "error",
                            "data": str(e),
                        }
                    )

                    await manager.send_end(websocket)

                    await websocket.close(code=1011)
            except Exception:
                logger.warning("Failed to send error message to client.")

        finally:
            manager.disconnect(websocket)
            db.close()
