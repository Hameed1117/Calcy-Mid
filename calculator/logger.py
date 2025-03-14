"""
logger.py
Singleton logger, reading environment variables: LOG_LEVEL, LOG_FILE.
Design Pattern Used: Singleton.
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
            log_file = os.environ.get("LOG_FILE", "").strip()

            logger = logging.getLogger("AdvancedCalculatorLogger")
            logger.setLevel(log_level)

            if not logger.handlers:
                formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
                if log_file:
                    file_handler = logging.FileHandler(log_file)
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                else:
                    console_handler = logging.StreamHandler()
                    console_handler.setFormatter(formatter)
                    logger.addHandler(console_handler)

            cls._instance = logger
        return cls._instance
