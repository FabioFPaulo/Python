from time import time
import cv2
import mediapipe as mp


class Recognizer:
    def __init__(self, model_path: str):
        self.model_path = model_path

        self.base_options = mp.tasks.BaseOptions(model_asset_path=self.model_path)
        self.hand_landmarks = []

        def print_result(
            result: mp.tasks.vision.HandLandmarkerResult,  # type: ignore
            output_image: mp.Image,
            timestamp_ms: int,
        ):
            if result.hand_landmarks and len(result.hand_landmarks) > 0:
                self.hand_landmarks = result.hand_landmarks[0]
                print(self.hand_landmarks[12])
            else:
                self.hand_landmarks = []

        self.options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=self.base_options,
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback=print_result,
            min_hand_detection_confidence=0.7,
        )

        self.create_landmark()

    def create_landmark(self):
        self.landmarker = mp.tasks.vision.HandLandmarker.create_from_options(
            self.options
        )

    def remove_landmark(self):
        if getattr(self, "landmarker", None):
            try:
                self.landmarker.close()
            except Exception:
                pass
            self.landmarker = None

    def recognize(self, frame: cv2.typing.MatLike):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = Recognizer.convert_frame(image)
        self.landmarker.detect_async(mp_image, int(time() * 1000))

        # draw hand connections
        mp.tasks.vision.drawing_utils.draw_landmarks(
            frame,
            self.hand_landmarks,
            mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS,
        )

    @staticmethod
    def convert_frame(frame: cv2.typing.MatLike) -> mp.Image:
        return mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
