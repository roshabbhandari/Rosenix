from collections import OrderedDict
from typing import Generic, TypeVar

T = TypeVar("T")

class LRUCache(Generic[T]):
    def __init__(self, capacity: int = 128):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._items: OrderedDict[str, T] = OrderedDict()

    def get(self, key: str, default=None):
        if key not in self._items:
            return default
        value = self._items.pop(key)
        self._items[key] = value
        return value

    def set(self, key: str, value: T) -> None:
        self._items.pop(key, None)
        self._items[key] = value
        while len(self._items) > self.capacity:
            self._items.popitem(last=False)

    def __len__(self) -> int:
        return len(self._items)
