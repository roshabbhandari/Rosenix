"""LLM provider protocol.

Any class implementing `complete` and `stream` with this shape satisfies
`LLMProvider` — including classes that never import this module. This is
what "no vendor lock-in" means concretely: the framework depends on a
*shape*, not a base class from a specific package.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Literal, Protocol, runtime_checkable

from pydantic import BaseModel

Role = Literal["system", "user", "assistant", "tool"]


class Message(BaseModel):
    """A single turn in a conversation. Immutable, serializable, typed."""

    role: Role
    content: str
    name: str | None = None
    tool_call_id: str | None = None


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class Completion(BaseModel):
    """A finished (non-streamed) model response."""

    content: str
    role: Role = "assistant"
    model: str
    usage: Usage = Usage()
    finish_reason: str | None = None
    raw: dict | None = None  # original provider payload, for escape-hatch access


class Chunk(BaseModel):
    """One piece of a streamed response."""

    delta: str
    model: str
    finish_reason: str | None = None


@runtime_checkable
class LLMProvider(Protocol):
    """Structural contract for any chat-completion-capable LLM backend.

    Implement this with a plain class — no inheritance from this
    Protocol is required, `isinstance()` checks work anyway because it
    is `@runtime_checkable`.
    """

    async def complete(self, messages: list[Message], **kwargs: object) -> Completion:
        """Return a single, complete response for the given conversation."""
        ...

    def stream(self, messages: list[Message], **kwargs: object) -> AsyncIterator[Chunk]:
        """Yield the response incrementally as it is generated."""
        ...
