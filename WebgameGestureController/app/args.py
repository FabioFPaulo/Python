import argparse


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="Game Gesture Controller")
        parser.add_argument(
            "-ci",
            "--cam_idx",
            default=0,
            type=int,
            help="Index of cameras, use 'ls /dev/video*' to get the index",
        )
        parser.add_argument(
            "-m",
            "--model",
            type=str,
            default="./app/models/hand_landmarker.task",
            help="Model for hand recognition",
        )

        _args = parser.parse_args()

        self.cam_idx: int = _args.cam_idx
        self.model: str = _args.model

    def __str__(self):
        return f"""Arguments:
    cam_idx: {self.cam_idx}
    model: {self.model}
"""
