from dataclasses import dataclass

@dataclass(slots=True)
class AgentState:
    status: str = "idle"
    step: int = 0
    error: str | None = None

    def fail(self, error: str) -> None:
        self.status = "failed"
        self.error = error
