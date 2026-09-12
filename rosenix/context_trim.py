from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")

def trim_recent(items: Sequence[T], limit: int) -> list[T]:
    if limit <= 0:
        return []
    return list(items[-limit:])

def trim_text(value: str, limit: int) -> str:
    if limit <= 0:
        return ""
    return value if len(value) <= limit else value[:limit]
