import asyncio
from app.camera import CameraHandler
from app.server import SocketServer


async def main():
    camera = CameraHandler()
    server = SocketServer()

    # Create concurrent tasks
    print("Starting system....")
    await asyncio.gather(camera.run(), server.run())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("System stopped.")
