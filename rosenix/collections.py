from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")

def unique(items: Iterable[T]) -> list[T]:
    return list(dict.fromkeys(items))

def first(items: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(items), default)
