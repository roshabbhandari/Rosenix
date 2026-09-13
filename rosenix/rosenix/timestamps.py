from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc)


def to_iso(value):
    if not isinstance(value, datetime):
        raise TypeError("value must be a datetime")
    return value.isoformat()
