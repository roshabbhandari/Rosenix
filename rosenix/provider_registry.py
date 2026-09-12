from .providers import ModelProvider

class ProviderRegistry:
    def __init__(self):
        self._providers: dict[str, ModelProvider] = {}

    def register(self, name: str, provider: ModelProvider) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("provider name is required")
        self._providers[key] = provider

    def get(self, name: str) -> ModelProvider | None:
        return self._providers.get(name.strip().lower())

    def names(self) -> tuple[str, ...]:
        return tuple(self._providers)
