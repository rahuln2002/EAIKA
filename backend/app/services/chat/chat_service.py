from sqlalchemy.orm import Session

from app.db.models.chat import Chat
from app.db.models.message import Message
from app.rag.pipelines.rag_pipeline import (
    RAGPipeline,
)


class ChatService:
    """
    Persistent chat service.
    """

    @staticmethod
    def create_chat(
        db: Session,
        user_id: int,
    ) -> Chat:
        """
        Create chat session.
        """

        chat = Chat(
            user_id=user_id,
        )

        db.add(chat)

        db.commit()

        db.refresh(chat)

        return chat

    @staticmethod
    def save_message(
        db: Session,
        chat_id: int,
        role: str,
        content: str,
    ) -> Message:
        """
        Save chat message.
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
    def generate_rag_response(
        db: Session,
        chat_id: int,
        query: str,
    ) -> dict:
        """
        Generate and persist RAG response.
        """

        # =================================================
        # SAVE USER MESSAGE
        # =================================================

        ChatService.save_message(
            db=db,
            chat_id=chat_id,
            role="user",
            content=query,
        )

        # =================================================
        # RUN RAG
        # =================================================

        rag_pipeline = RAGPipeline()

        response = rag_pipeline.run(
            db=db,
            query=query,
        )

        answer = response["answer"]

        # =================================================
        # SAVE ASSISTANT MESSAGE
        # =================================================

        ChatService.save_message(
            db=db,
            chat_id=chat_id,
            role="assistant",
            content=answer,
        )

        return response
