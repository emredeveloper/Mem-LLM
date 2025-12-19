"""
Enhanced Logging System for Mem-LLM
====================================
Provides structured logging with different levels and output formats.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class MemLLMLogger:
    """Structured logger for Mem-LLM with file and console output"""

    def __init__(
        self,
        name: str = "mem_llm",
        log_file: Optional[str] = None,
        log_level: str = "INFO",
        console_output: bool = True,
    ):
        """
        Initialize logger

        Args:
            name: Logger name
            log_file: Path to log file (optional)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output: Enable console output
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Clear existing handlers
        self.logger.handlers = []

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # File handler
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str, **kwargs):
        """Debug level log"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_info}" if extra_info else message
        self.logger.debug(full_message)

    def info(self, message: str, **kwargs):
        """Info level log"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_info}" if extra_info else message
        self.logger.info(full_message)

    def warning(self, message: str, **kwargs):
        """Warning level log"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_info}" if extra_info else message
        self.logger.warning(full_message)

    def error(self, message: str, **kwargs):
        """Error level log"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_info}" if extra_info else message
        self.logger.error(full_message)

    def critical(self, message: str, **kwargs):
        """Critical level log"""
        extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_info}" if extra_info else message
        self.logger.critical(full_message)

    def log_llm_call(self, model: str, prompt_length: int, response_length: int, duration: float):
        """Log LLM API call with metrics"""
        self.info(
            "LLM API Call",
            model=model,
            prompt_tokens=prompt_length,
            response_tokens=response_length,
            duration_ms=f"{duration*1000:.2f}",
        )

    def log_memory_operation(self, operation: str, user_id: str, success: bool, details: str = ""):
        """Log memory operations"""
        level = self.info if success else self.error
        level(f"Memory {operation}", user_id=user_id, success=success, details=details)

    def log_error_with_context(self, error: Exception, context: dict):
        """Log error with full context"""
        self.error(f"Exception: {type(error).__name__}: {str(error)}", **context)


def get_logger(
    name: str = "mem_llm", log_file: Optional[str] = "logs/mem_llm.log", log_level: str = "INFO"
) -> MemLLMLogger:
    """
    Get or create logger instance

    Args:
        name: Logger name
        log_file: Log file path
        log_level: Logging level

    Returns:
        MemLLMLogger instance
    """
    return MemLLMLogger(name=name, log_file=log_file, log_level=log_level)
