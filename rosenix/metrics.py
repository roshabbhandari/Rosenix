from dataclasses import dataclass, field
from time import monotonic

@dataclass
class Counter:
    value: int = 0
    def inc(self, amount: int = 1) -> int:
        self.value += amount
        return self.value

@dataclass
class Timer:
    started: float = field(default_factory=monotonic)
    def elapsed(self) -> float:
        return monotonic() - self.started
