from .providers import ModelProvider

class AgentRouter:
    def __init__(self, providers: list[ModelProvider] | None = None):
        self.providers = providers or []

    def choose(self, preferred: str | None = None) -> ModelProvider | None:
        if preferred:
            for provider in self.providers:
                if provider.name == preferred:
                    return provider
        return self.providers[0] if self.providers else None
