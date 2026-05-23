from fastapi import WebSocket


class ConnectionManager:
    """
    WebSocket connection manager.
    """

    def __init__(
        self,
    ) -> None:
        self.active_connections = []

    async def connect(
        self,
        websocket: WebSocket,
    ):
        """
        Accept connection.
        """

        await websocket.accept()

        self.active_connections.append(websocket)

    def disconnect(
        self,
        websocket: WebSocket,
    ):
        """
        Remove connection.
        """

        self.active_connections.remove(websocket)

    async def send_token(
        self,
        websocket: WebSocket,
        token: str,
    ):

        await websocket.send_json(
            {
                "type": "token",
                "data": token,
            }
        )

    async def send_end(
        self,
        websocket: WebSocket,
    ):

        await websocket.send_json(
            {
                "type": "end",
            }
        )

    async def send_sources(
        self,
        websocket: WebSocket,
        sources,
    ):

        await websocket.send_json(
            {
                "type": "sources",
                "data": sources,
            }
        )

    async def send_chat_id(
        self,
        websocket: WebSocket,
        chat_id: int,
    ):

        await websocket.send_json(
            {
                "type": "chat_id",
                "data": chat_id,
            }
        )
