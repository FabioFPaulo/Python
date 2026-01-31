class CameraNotFoundError(Exception):
    def __init__(self, cam_idx, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(f"Camera with index {cam_idx} not found!")

        # Now for your custom code...
        self.errors = errors
