from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def utc_timestamp() -> float:
    return utc_now().timestamp()
