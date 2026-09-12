from dataclasses import dataclass
from datetime import datetime
from .clock import utc_now

@dataclass(frozen=True)
class HealthStatus:
    healthy: bool
    checked_at: datetime
    detail: str = ""

def healthy(detail: str = "ok") -> HealthStatus:
    return HealthStatus(True, utc_now(), detail)

def unhealthy(detail: str) -> HealthStatus:
    return HealthStatus(False, utc_now(), detail)
