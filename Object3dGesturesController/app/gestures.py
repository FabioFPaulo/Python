import asyncio
from time import time
from typing import Callable
from cv2.typing import MatLike
import cv2 as cv
import mediapipe as mp


class Gestures:
    def __init__(
        self,
        model_path: str = None,
        broadcast_callback: Callable[[str], None] | None = None,
    ):
        self.model_path = model_path or "./app/models/hand_landmarker.task"
        self.base_options = mp.tasks.BaseOptions(model_asset_path=self.model_path)
        self.hand_landmarks = []

        self.options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=self.base_options,
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=self.print_result,
            min_hand_detection_confidence=0.7,
        )

        self.broadcast = broadcast_callback

        self.landmarker = None
        self._create_landmarker()

    def print_result(
        self,
        result: mp.tasks.vision.HandLandmarkerResult,  # type: ignore
        output_image: mp.Image,
        timestamp_ms: int,
    ):
        if result.hand_landmarks and len(result.hand_landmarks) > 0:
            self.hand_landmarks = result.hand_landmarks[0]

            if self.broadcast:
                asyncio.run(self.broadcast(str(self.hand_landmarks[7].x)))

    def recognize(self, frame: MatLike):
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = Gestures.convert_frame(image)
        self.landmarker.detect_async(mp_image, int(time() * 1000))

        # draw hand connections
        mp.tasks.vision.drawing_utils.draw_landmarks(
            frame,
            self.hand_landmarks,
            mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS,
        )

    def _create_landmarker(self):
        self.landmarker = mp.tasks.vision.HandLandmarker.create_from_options(
            self.options
        )

    def _remove_landmarker(self):
        if getattr(self, "landmarker", None):
            try:
                self.landmarker.close()
            except Exception:
                pass
            self.landmarker = None

    @staticmethod
    def convert_frame(frame: cv.typing.MatLike) -> mp.Image:
        return mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
