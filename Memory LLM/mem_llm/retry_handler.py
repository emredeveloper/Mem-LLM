"""
Retry Logic with Exponential Backoff
====================================
Robust error handling for LLM API calls and database operations.
"""

import functools
import logging
import time
from typing import Callable, Optional, Tuple, Type


def exponential_backoff_retry(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    logger: Optional[logging.Logger] = None,
):
    """
    Decorator for retrying functions with exponential backoff

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        exponential_base: Base for exponential calculation
        max_delay: Maximum delay between retries
        exceptions: Tuple of exceptions to catch and retry
        logger: Optional logger for retry information

    Example:
        @exponential_backoff_retry(max_retries=3, initial_delay=1.0)
        def unstable_api_call():
            # Your code here
            pass
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        if logger:
                            logger.error(
                                f"Function {func.__name__} failed after {max_retries} "
                                f"retries: {str(e)}"
                            )
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(initial_delay * (exponential_base**attempt), max_delay)

                    if logger:
                        logger.warning(
                            f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries}), "
                            f"retrying in {delay:.2f}s: {e}"
                        )

                    time.sleep(delay)

            # Should never reach here, but just in case
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


class SafeExecutor:
    """Safe execution wrapper with error handling and fallbacks"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    def execute_with_fallback(
        self,
        primary_func: Callable,
        fallback_func: Optional[Callable] = None,
        fallback_value: any = None,
        error_message: str = "Operation failed",
    ):
        """
        Execute function with fallback on error

        Args:
            primary_func: Main function to execute
            fallback_func: Fallback function if primary fails
            fallback_value: Value to return if both fail
            error_message: Error message prefix

        Returns:
            Result from primary_func, fallback_func, or fallback_value
        """
        try:
            return primary_func()
        except Exception as e:
            self.logger.error(f"{error_message}: {str(e)}")

            if fallback_func:
                try:
                    self.logger.info("Attempting fallback function")
                    return fallback_func()
                except Exception as fallback_e:
                    self.logger.error(f"Fallback also failed: {str(fallback_e)}")

            return fallback_value

    def safe_json_parse(self, json_string: str, default: dict = None) -> dict:
        """
        Safely parse JSON with fallback

        Args:
            json_string: JSON string to parse
            default: Default value if parsing fails

        Returns:
            Parsed dict or default
        """
        import json

        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse error: {str(e)}")

            # Try to extract partial JSON
            try:
                # Find first { and last }
                start = json_string.find("{")
                end = json_string.rfind("}")
                if start != -1 and end != -1:
                    partial = json_string[start : end + 1]
                    return json.loads(partial)
            except Exception:
                pass

            return default if default is not None else {}

    def safe_db_operation(
        self,
        operation: Callable,
        operation_name: str = "Database operation",
        default_value: any = None,
    ):
        """
        Safely execute database operation

        Args:
            operation: Database operation function
            operation_name: Name for logging
            default_value: Value to return on failure

        Returns:
            Operation result or default_value
        """
        try:
            return operation()
        except Exception as e:
            self.logger.error(f"{operation_name} failed: {str(e)}")
            return default_value


# Connection checker with retry
def check_connection_with_retry(url: str, max_retries: int = 3, timeout: int = 5) -> bool:
    """
    Check connection with retry logic

    Args:
        url: URL to check
        max_retries: Maximum retry attempts
        timeout: Request timeout

    Returns:
        True if connection successful
    """
    import requests

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return True
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(1.0 * (2**attempt))
            continue

    return False
