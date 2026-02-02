import asyncio
from typing import override
from utils.task import BaseTask


class SocketServer(BaseTask):
    def __init__(self):
        super().__init__()

    @override
    async def run(self):
        print("Server started")
        await asyncio.Future()
