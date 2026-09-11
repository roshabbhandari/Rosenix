from dataclasses import dataclass
from typing import Callable, Any

@dataclass(slots=True)
class Tool:
    name: str
    handler: Callable[..., Any]

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)
