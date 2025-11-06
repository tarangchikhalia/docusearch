"""Logging configuration for the RAG system."""
import logging
import sys
from pathlib import Path
from typing import Optional

from src.config import Config


class Logger:
    """Custom logger for the RAG system."""

    _loggers = {}

    @classmethod
    def get_logger(cls, name: str, log_file: Optional[Path] = None) -> logging.Logger:
        """Get or create a logger with the specified name.

        Args:
            name: Logger name
            log_file: Optional file path for logging

        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))

        # Remove existing handlers
        logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        cls._loggers[name] = logger
        return logger


def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    return Logger.get_logger(name)
