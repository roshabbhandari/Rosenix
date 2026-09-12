from collections.abc import Callable
from typing import Any

Hook = Callable[..., Any]

class HookRegistry:
    def __init__(self):
        self._hooks: dict[str, list[Hook]] = {}

    def register(self, event: str, hook: Hook) -> None:
        self._hooks.setdefault(event, []).append(hook)

    def emit(self, event: str, **payload: Any) -> list[Any]:
        return [hook(**payload) for hook in self._hooks.get(event, [])]
