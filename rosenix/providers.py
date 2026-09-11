from dataclasses import dataclass

@dataclass(slots=True)
class ModelProvider:
    name: str
    model: str
    base_url: str | None = None

    def endpoint(self) -> str | None:
        return self.base_url.rstrip("/") if self.base_url else None
