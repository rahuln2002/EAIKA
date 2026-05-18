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

    async def send_message(
        self,
        websocket: WebSocket,
        message: str,
    ):
        """
        Send message to client.
        """

        await websocket.send_text(message)
