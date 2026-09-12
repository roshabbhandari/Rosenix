from typing import Any

def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")
    return value.strip()

def require_positive(value: int, field: str) -> int:
    if value <= 0:
        raise ValueError(f"{field} must be positive")
    return value
