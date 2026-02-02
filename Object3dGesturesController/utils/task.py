import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys


class BaseTask:
    def __init__(self, log_name="app", log_path="app", log_level=logging.INFO):
        self.logger = self._setup_logger(log_name, log_path, log_level)

    async def run(self): ...

    def _setup_logger(self, name: str, folder_path: str, level=logging.INFO):
        # 1. Construct the full directory path
        # folder_path might be "classA", so log_dir becomes "logs/classA"
        log_dir = os.path.join("logs", folder_path)

        # 2. Ensure the directory exists
        os.makedirs(log_dir, exist_ok=True)

        # 3. Create the full path to the FILE inside that directory
        # This was the missing link in your snippet
        log_file = os.path.join(log_dir, "app.log")

        # 4. Setup the Rotating Handler
        handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
        )
        handler.suffix = "%Y-%m-%d"

        stream_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        handler.setFormatter(formatter)

        # 5. Get the logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 6. CRITICAL: Only add the handler if it's not already there
        # This prevents the same message appearing multiple times
        if not logger.handlers:
            logger.addHandler(handler)
            logger.addHandler(stream_handler)

        return logger
