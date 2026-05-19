from sqlalchemy.orm import Session
from sqlalchemy import desc

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
        user_id: int,
    ) -> dict:
        """
        Generate conversational RAG response.
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
        # GET CONVERSATION HISTORY
        # =================================================

        history = ChatService.get_chat_history(
            db=db,
            chat_id=chat_id,
        )

        # =================================================
        # RUN RAG
        # =================================================

        rag_pipeline = RAGPipeline()

        response = rag_pipeline.run(
            db=db,
            query=query,
            conversation_history=history,
            user_id=user_id,
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

    @staticmethod
    def get_chat_history(
        db: Session,
        chat_id: int,
        limit: int = 10,
    ) -> list[str]:
        """
        Retrieve recent conversation history.
        """

        messages = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(desc(Message.id))
            .limit(limit)
            .all()
        )

        messages.reverse()

        history = []

        for message in messages:
            history.append(f"{message.role}: {message.content}")

        return history
