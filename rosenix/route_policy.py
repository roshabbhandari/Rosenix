from dataclasses import dataclass

@dataclass(frozen=True)
class RoutePolicy:
    preferred: tuple[str, ...] = ()
    fallback: tuple[str, ...] = ()
    max_attempts: int = 2

    def candidates(self) -> tuple[str, ...]:
        ordered = list(self.preferred) + list(self.fallback)
        return tuple(dict.fromkeys(ordered))[: max(0, self.max_attempts)]
