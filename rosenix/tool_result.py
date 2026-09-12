from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ToolResult:
    success: bool
    output: Any = None
    error: str | None = None

    @classmethod
    def ok(cls, output: Any = None) -> "ToolResult":
        return cls(True, output=output)

    @classmethod
    def fail(cls, error: str) -> "ToolResult":
        return cls(False, error=error)
