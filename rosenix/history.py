from collections import deque

class TaskHistory:
    def __init__(self, limit: int = 100):
        self._items = deque(maxlen=max(1, limit))

    def add(self, task_id: str) -> None:
        self._items.append(task_id)

    def all(self) -> list[str]:
        return list(self._items)
