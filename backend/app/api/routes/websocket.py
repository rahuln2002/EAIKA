from app.websockets.websocket_handler import (
    WebSocketHandler,
)
from fastapi import (
    APIRouter,
    Query,
    WebSocket,
)

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    token: str = Query(...),
):
    """
    Streaming AI WebSocket endpoint.
    """

    await WebSocketHandler.handle_chat(
        websocket=websocket,
        token=token,
    )
