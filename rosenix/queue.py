from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")

class BoundedQueue(Generic[T]):
    def __init__(self, capacity: int = 100):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._items: deque[T] = deque(maxlen=capacity)

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T | None:
        return self._items.popleft() if self._items else None

    def __len__(self) -> int:
        return len(self._items)
