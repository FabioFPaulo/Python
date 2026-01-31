import cv2 as cv

from app.errors.camera_errors import CameraNotFoundError


class Capture:
    def __init__(self, cam_idx=0):
        self.cam_idx = cam_idx

    def run(self, recognize_callback):
        cap = cv.VideoCapture(self.cam_idx)

        if not cap.isOpened():
            raise CameraNotFoundError(self.cam_idx)
        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                frame = cv.flip(frame, 1)

                recognize_callback(frame)

                cv.imshow("Game Gesture Controller", frame)
                if cv.waitKey(1) == ord("q"):
                    break

        finally:
            cap.release()
            cv.destroyAllWindows()
