from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.api.dependencies.database import (
    get_db,
)
from app.services.chat.chat_service import (
    ChatService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
async def chat(
    query: str,
    chat_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Conversational RAG endpoint.
    """

    # =====================================================
    # CREATE NEW CHAT IF NEEDED
    # =====================================================

    if chat_id is None:
        chat_session = ChatService.create_chat(
            db=db,
            user_id=int(current_user["sub"]),
        )

        chat_id = chat_session.id

    # =====================================================
    # GENERATE RESPONSE
    # =====================================================

    response = ChatService.generate_rag_response(
        db=db,
        chat_id=chat_id,
        query=query,
    )

    return {
        "chat_id": chat_id,
        "response": response,
    }


@router.get("/{chat_id}")
async def get_chat_history(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve chat history.
    """

    history = ChatService.get_chat_history(
        db=db,
        chat_id=chat_id,
        limit=50,
    )

    return {
        "chat_id": chat_id,
        "messages": history,
    }
