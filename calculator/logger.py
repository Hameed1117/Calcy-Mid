"""
logger.py
Singleton logger, reading environment variables: LOG_LEVEL, LOG_FILE.
Design Pattern Used: Singleton.
If LOG_FILE is not provided, logs are saved to "logs/app.log".
"""

import logging
import os
from typing import Optional

class LoggerSingleton:
    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._instance is None:
            log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            log_level = log_level_str if log_level_str in valid_levels else "INFO"
            log_file = os.environ.get("LOG_FILE")
            if not log_file:
                # Use a default log file in the "logs" folder if LOG_FILE is not provided.
                log_dir = "logs"
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                log_file = os.path.join(log_dir, "app.log")

            logger = logging.getLogger("AdvancedCalculatorLogger")
            logger.setLevel(log_level)

            if not logger.handlers:
                formatter = logging.Formatter(
                    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
                )
                # File handler for persistent logging.
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                # Console handler for immediate output.
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            cls._instance = logger
        return cls._instance
