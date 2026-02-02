import asyncio
from typing import Callable, override

import cv2 as cv
from app.gestures import Gestures
from errors.camera_errors import CameraNotFoundError
from utils.task import BaseTask


class CameraHandler(BaseTask):
    def __init__(
        self,
        broadcast_callback: Callable[[str], str],
        cam_idx=0,
    ):
        super().__init__(log_name="CameraHandler", log_path="CameraHandler")

        self.bradcast_callback = broadcast_callback
        self.cam_idx = cam_idx
        self.gestures = Gestures()
        self.is_running = False

    def _capture(self):
        self.logger.info("Starting camera capture")
        cap = cv.VideoCapture(self.cam_idx)
        self.is_running = True

        if not cap.isOpened():
            raise CameraNotFoundError(self.cam_idx)

        try:
            while self.is_running:
                ret, frame = cap.read()

                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                frame = cv.flip(frame, 1)

                self.gestures.recognize(frame)

                cv.imshow("Game Gesture Controller", frame)
                if cv.waitKey(1) == ord("q"):
                    break
        finally:
            cap.release()
            cv.destroyAllWindows()

    @override
    async def run(self):
        # this is needed to can open camera in parallel with websocket
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._capture)
