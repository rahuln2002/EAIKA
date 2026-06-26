from app.core.constants.cache_constants import CHAT_PREFIX, CHAT_TTL
from app.cache.cache_manager import CacheManager
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.models.chat import Chat
from app.db.models.message import Message

from app.rag.pipelines.rag_pipeline import (
    RAGPipeline,
)


class ChatService:
    """
    Persistent conversational RAG service.
    """

    @staticmethod
    def _history_cache_key(
        chat_id: int,
    ) -> str:

        return f"{CHAT_PREFIX}:{chat_id}:history"

    @staticmethod
    def create_chat(
        db: Session,
        user_id: int,
        # title: str = "New Chat",
    ) -> Chat:
        """
        Create chat session.
        """

        chat = Chat(
            user_id=user_id,
            # title=title,
        )

        db.add(chat)

        db.commit()

        db.refresh(chat)

        return chat

    @staticmethod
    def get_chat(
        db: Session,
        chat_id: int,
        user_id: int,
    ) -> Chat | None:
        """
        Retrieve user-owned chat.
        """

        return (
            db.query(Chat)
            .filter(
                Chat.id == chat_id,
                Chat.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def save_message(
        db: Session,
        chat_id: int,
        role: str,
        content: str,
    ) -> Message:
        """
        Persist message.
        """

        message = Message(
            chat_id=chat_id,
            role=role,
            content=content,
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        cache_key = ChatService._history_cache_key(
            chat_id,
        )

        history = CacheManager.get(
            cache_key,
        )

        if history is not None:
            history = (
                history
                + [
                    {
                        "role": role,
                        "content": content,
                    }
                ]
            )[-20:]

            CacheManager.set(
                cache_key,
                history,
                expire=CHAT_TTL,
            )

        return message

    @staticmethod
    def get_chat_history(
        db: Session,
        chat_id: int,
        limit: int = 20,
    ) -> list[dict]:
        """
        Retrieve recent chat history.
        """

        cache_key = ChatService._history_cache_key(
            chat_id,
        )

        cached = CacheManager.get(
            cache_key,
        )

        if cached is not None:
            return cached

        messages = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(desc(Message.id))
            .limit(limit)
            .all()
        )

        messages.reverse()

        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

        CacheManager.set(
            cache_key,
            history,
            expire=CHAT_TTL,
        )

        return history

    @staticmethod
    def generate_rag_response(
        db: Session,
        chat_id: int,
        query: str,
        user_id: int,
    ) -> dict:
        """
        Generate conversational RAG response.
        """

        # =============================================
        # SAVE USER MESSAGE
        # =============================================

        ChatService.save_message(
            db=db,
            chat_id=chat_id,
            role="user",
            content=query,
        )

        # =============================================
        # CONVERSATION HISTORY
        # =============================================

        history = ChatService.get_chat_history(
            db=db,
            chat_id=chat_id,
        )

        # =============================================
        # RUN RAG
        # =============================================

        rag_pipeline = RAGPipeline()

        response = rag_pipeline.run(
            db=db,
            query=query,
            conversation_history=history,
            user_id=user_id,
        )

        answer = response["answer"]

        # =============================================
        # SAVE ASSISTANT RESPONSE
        # =============================================

        ChatService.save_message(
            db=db,
            chat_id=chat_id,
            role="assistant",
            content=answer,
        )

        return response

    @staticmethod
    def list_user_chats(
        db: Session,
        user_id: int,
    ) -> list[dict]:
        """
        Retrieve user chats.
        """

        chats = (
            db.query(Chat).filter(Chat.user_id == user_id).order_by(desc(Chat.id)).all()
        )

        return [
            {
                "id": chat.id,
                # "title": chat.title,
            }
            for chat in chats
        ]
