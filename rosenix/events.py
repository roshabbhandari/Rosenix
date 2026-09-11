from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True, slots=True)
class AgentEvent:
    kind: str
    data: dict
    created_at: datetime

    @classmethod
    def create(cls, kind: str, data: dict | None = None) -> "AgentEvent":
        return cls(kind, data or {}, datetime.now(timezone.utc))
