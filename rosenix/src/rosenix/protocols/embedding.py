"""Embedding provider protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Structural contract for turning text into vectors."""

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text, same order."""
        ...

    @property
    def dimensions(self) -> int:
        """Length of each returned embedding vector."""
        ...
