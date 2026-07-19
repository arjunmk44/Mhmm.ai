"""
Logging utility for AI/ML module.
Provides structured logging for pipelines, agents, and API calls.
"""

import logging
import sys
from ai_ml.config.settings import settings


def get_logger(name: str = "ai_ml") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
        logger.setLevel(log_level)
    return logger


logger = get_logger("ai_ml")
