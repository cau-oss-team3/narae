from fastapi import WebSocket


class WebsocketConnectionManager:
    """
    Class for websocket events
    """

    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_direct_message(self, message: str, websocket: WebSocket):
        """
        Send message to specific websocket
        """
        await websocket.send_text(message)

    async def send_broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)

    def is_connected(self, websocket: WebSocket):
        return websocket in self.connections


def get_websocket_manager():
    return WebsocketConnectionManager()
