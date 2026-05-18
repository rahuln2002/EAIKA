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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Persistent RAG chat endpoint.
    """

    # =====================================================
    # CREATE CHAT SESSION
    # =====================================================

    chat_session = ChatService.create_chat(
        db=db,
        user_id=current_user["sub"],
    )

    # =====================================================
    # GENERATE RESPONSE
    # =====================================================

    response = ChatService.generate_rag_response(
        db=db,
        chat_id=chat_session.id,
        query=query,
    )

    return {
        "chat_id": chat_session.id,
        "response": response,
    }
