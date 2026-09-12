from collections import defaultdict
from collections.abc import Callable
from typing import Any

class EventBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, event: str, listener: Callable[..., Any]) -> None:
        self._listeners[event].append(listener)

    def publish(self, event: str, **payload: Any) -> list[Any]:
        return [listener(**payload) for listener in tuple(self._listeners[event])]

    def clear(self, event: str | None = None) -> None:
        if event is None:
            self._listeners.clear()
        else:
            self._listeners.pop(event, None)
