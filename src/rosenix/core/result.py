from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass(frozen=True)
class Result(Generic[T]):
    value: T | None = None
    error: Exception | None = None

    @property
    def ok(self):
        return self.error is None
