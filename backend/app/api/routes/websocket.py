from fastapi import APIRouter
from fastapi import WebSocket

from app.websockets.websocket_handler import (
    WebSocketHandler,
)

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
):
    """
    Streaming AI WebSocket endpoint.
    """

    await WebSocketHandler.handle_chat(websocket)
