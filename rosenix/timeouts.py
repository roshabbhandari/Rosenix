from dataclasses import dataclass

@dataclass(frozen=True)
class TimeoutPolicy:
    connect: float = 10.0
    read: float = 60.0
    total: float = 120.0

    def validate(self) -> "TimeoutPolicy":
        if min(self.connect, self.read, self.total) <= 0:
            raise ValueError("timeouts must be positive")
        if self.total < self.connect:
            raise ValueError("total timeout cannot be below connect timeout")
        return self
