from dataclasses import dataclass, field
from uuid import uuid4

@dataclass(slots=True)
class AgentTask:
    prompt: str
    id: str = field(default_factory=lambda: uuid4().hex)
    status: str = "pending"
