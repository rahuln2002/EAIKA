from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)

from app.api.dependencies.database import (
    get_db,
)

from app.db.schemas.chat_schema import (
    ChatRequest,
    ConversationalChatResponse,
    ChatHistoryResponse,
    ChatListResponse,
)

from app.services.chat.chat_service import (
    ChatService,
)

from app.utils.citation_formatter import (
    format_sources,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

# =====================================================
# CHAT COMPLETION
# =====================================================


@router.post(
    "/",
    response_model=(ConversationalChatResponse),
)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Conversational RAG endpoint.
    """

    user_id = int(current_user["sub"])

    # ================================================
    # CREATE OR LOAD CHAT
    # ================================================

    if request.chat_id:
        chat_session = ChatService.get_chat(
            db=db,
            chat_id=request.chat_id,
            user_id=user_id,
        )

        if not chat_session:
            raise HTTPException(
                status_code=404,
                detail="Chat not found.",
            )

    else:
        title = request.query[:50] if request.query else "New Chat"

        chat_session = ChatService.create_chat(
            db=db,
            user_id=user_id,
            title=title,
        )

    # ================================================
    # GENERATE RESPONSE
    # ================================================

    response = ChatService.generate_rag_response(
        db=db,
        chat_id=chat_session.id,
        query=request.query,
        user_id=user_id,
    )

    return {
        "chat_id": chat_session.id,
        "answer": response["answer"],
        "sources": format_sources(response["sources"]),
        "evaluation": response["evaluation"],
    }


# =====================================================
# CHAT HISTORY
# =====================================================


@router.get(
    "/{chat_id}",
    response_model=ChatHistoryResponse,
)
async def get_chat_history(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve chat history.
    """

    user_id = int(current_user["sub"])

    # ================================================
    # OWNERSHIP VALIDATION
    # ================================================

    chat = ChatService.get_chat(
        db=db,
        chat_id=chat_id,
        user_id=user_id,
    )

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found.",
        )

    history = ChatService.get_chat_history(
        db=db,
        chat_id=chat_id,
        limit=50,
    )

    return {
        "chat_id": chat_id,
        "messages": history,
    }


# =====================================================
# LIST USER CHATS
# =====================================================


@router.get(
    "/list",
    response_model=list[ChatListResponse],
)
async def list_chats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    List user chats.
    """

    user_id = int(current_user["sub"])

    chats = ChatService.list_user_chats(
        db=db,
        user_id=user_id,
    )

    return chats
