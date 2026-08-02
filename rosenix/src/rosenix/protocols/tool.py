"""Tool protocol.

A Tool is anything an agent can call: a function wrapped by
`@tool` (see `rosenix.kits.tool_decorator`), or any object
implementing this shape directly.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel


class ToolSpec(BaseModel):
    """Machine-readable description of a tool, used to build LLM function-
    calling schemas without depending on any one provider's exact format.
    """

    name: str
    description: str
    parameters: dict  # JSON Schema for the tool's arguments


@runtime_checkable
class Tool(Protocol):
    """Structural contract for anything an agent can invoke as a tool."""

    @property
    def spec(self) -> ToolSpec:
        """Static description of this tool's name, purpose, and arguments."""
        ...

    async def __call__(self, **kwargs: Any) -> Any:
        """Execute the tool with validated arguments and return a result."""
        ...
