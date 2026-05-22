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
    def create_chat(
        db: Session,
        user_id: int,
        title: str = "New Chat",
    ) -> Chat:
        """
        Create chat session.
        """

        chat = Chat(
            owner_id=user_id,
            title=title,
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
                Chat.owner_id == user_id,
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

        return message

    @staticmethod
    def get_chat_history(
        db: Session,
        chat_id: int,
        limit: int = 10,
    ) -> list[dict]:
        """
        Retrieve recent chat history.
        """

        messages = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(desc(Message.id))
            .limit(limit)
            .all()
        )

        messages.reverse()

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

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
    ):
        """
        Retrieve user chats.
        """

        chats = (
            db.query(Chat)
            .filter(Chat.owner_id == user_id)
            .order_by(desc(Chat.id))
            .all()
        )

        return [
            {
                "id": chat.id,
                "title": chat.title,
            }
            for chat in chats
        ]
