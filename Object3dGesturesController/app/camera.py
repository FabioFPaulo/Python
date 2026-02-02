import asyncio
from typing import override
from utils.task import BaseTask


class CameraHandler(BaseTask):
    def __init__(self):
        super().__init__()

    @override
    async def run(self):
        print("Camera started")
        await asyncio.Future()
