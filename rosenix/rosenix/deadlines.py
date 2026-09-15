from datetime import datetime, timedelta


def deadline_after(seconds, now=None):
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    base = now or datetime.now()
    return base + timedelta(seconds=seconds)


def is_expired(deadline, now=None):
    return (now or datetime.now()) >= deadline
