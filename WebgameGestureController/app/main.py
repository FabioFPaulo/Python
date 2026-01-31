from app.args import Args
from app.capture import Capture
from app.recognizer import Recognizer


def start_app():
    args = Args()
    print(args)

    # recognizer = Recognizer(args.model)
    # for frame in recognizer.start(args.cam_idx):
    #     cv.imshow("Game Gesture Controller", frame)
    #     if cv.waitKey(1) == ord("q"):
    #         break

    cap = Capture(args.cam_idx)
    recognizer = Recognizer(args.model)

    cap.run(recognizer.recognize)
