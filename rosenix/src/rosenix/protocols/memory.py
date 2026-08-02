"""Memory protocol.

Deliberately minimal: a Memory is just an ordered, appendable message
log. Summarization, windowing, or vector-backed recall are built as
separate composable strategies on top of this, not baked in here —
keeps the contract small and stable.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from rosenix.protocols.llm import Message


@runtime_checkable
class Memory(Protocol):
    """Structural contract for conversation history storage."""

    async def append(self, message: Message) -> None:
        """Add a message to the end of the history."""
        ...

    async def history(self) -> list[Message]:
        """Return all stored messages, oldest first."""
        ...

    async def clear(self) -> None:
        """Remove all stored messages."""
        ...
