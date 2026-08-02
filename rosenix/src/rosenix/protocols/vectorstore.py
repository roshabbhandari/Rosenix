"""Vector store protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel


class VectorRecord(BaseModel):
    id: str
    vector: list[float]
    metadata: dict = {}
    score: float | None = None  # populated on query results, ignored on upsert


@runtime_checkable
class VectorStore(Protocol):
    """Structural contract for a similarity-search-capable store."""

    async def upsert(self, records: list[VectorRecord]) -> None:
        """Insert or update records by id."""
        ...

    async def query(self, vector: list[float], top_k: int = 10) -> list[VectorRecord]:
        """Return the `top_k` most similar records, scored, best first."""
        ...

    async def delete(self, ids: list[str]) -> None:
        """Remove records by id. Silently ignores unknown ids."""
        ...
