import asyncio
from typing import override

from websockets import ConnectionClosed, ServerConnection, broadcast as bc, serve
from utils.task import BaseTask


# echo -e "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n" | nc 127.0.0.1 8765


class SocketServer(BaseTask):
    def __init__(self, host: str = "0.0.0.0", port=8765):
        super().__init__(log_name="SocketServer", log_path="SocketServer")

        self.host = host
        self.port = port

        self.connections = set()

    async def handle(self, websocket: ServerConnection):
        self.connections.add(websocket)
        self.logger.info(f"New Connection:\t{websocket.id}")
        try:
            await websocket.wait_closed()
        except Exception as e:
            self.logger.error(f"Error: {e}")
        finally:
            self.logger.info(f"Connection Closed:\t{websocket.id}")
            self.connections.remove(websocket)

    async def broadcast(self, message: str):
        bc(self.connections, message)

    @override
    async def run(self):
        async with serve(self.handle, self.host, self.port) as server:
            self.logger.info(f"Socket started on ws://{self.host}:{self.port}")
            await server.serve_forever()
