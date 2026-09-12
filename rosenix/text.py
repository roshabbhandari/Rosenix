def clean_text(value: str) -> str:
    return " ".join(value.replace("\r\n", "\n").split())

def truncate(value: str, limit: int, suffix: str = "…") -> str:
    if limit < 0:
        raise ValueError("limit must be non-negative")
    if len(value) <= limit:
        return value
    if not suffix or limit <= len(suffix):
        return value[:limit]
    return value[: limit - len(suffix)] + suffix
