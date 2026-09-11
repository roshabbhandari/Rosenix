import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

def retry(call: Callable[[], T], attempts: int = 3, delay: float = 0.5) -> T:
    attempts = max(1, attempts)
    last_error = None
    for index in range(attempts):
        try:
            return call()
        except Exception as exc:
            last_error = exc
            if index + 1 < attempts:
                time.sleep(delay)
    raise last_error
