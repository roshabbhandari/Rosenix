from dataclasses import dataclass

@dataclass(slots=True)
class RosenixConfig:
    model: str = "default"
    base_url: str | None = None
    timeout: float = 60.0
