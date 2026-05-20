from fastapi import (
    APIRouter,
    WebSocket,
    Query,
)

from app.websockets.websocket_handler import (
    WebSocketHandler,
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
