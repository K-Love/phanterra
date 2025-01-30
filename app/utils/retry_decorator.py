# app/utils/retry_decorator.py

import time
from functools import wraps
from typing import Callable, Any
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetryException(Exception):
    pass

def with_retry(
    max_attempts: int = 3,
    delay: int = 1,
    exponential_backoff: bool = True,
    allowed_exceptions: tuple = (Exception,)
) -> Callable:
    """
    Decorator for retrying operations with exponential backoff
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)

                except allowed_exceptions as e:
                    attempt += 1
                    if attempt == max_attempts:
                        logger.error(f"Final attempt failed for {func.__name__}: {str(e)}")
                        raise RetryException(f"Max attempts ({max_attempts}) reached: {str(e)}")

                    logger.warning(
                        f"Attempt {attempt} failed for {func.__name__}: {str(e)}. "
                        f"Retrying in {current_delay} seconds..."
                    )

                    time.sleep(current_delay)
                    if exponential_backoff:
                        current_delay *= 2

            return None
        return wrapper
    return decorator