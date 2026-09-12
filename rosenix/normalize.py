from urllib.parse import urlsplit, urlunsplit

def normalize_url(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    parsed = urlsplit(value if "://" in value else f"https://{value}")
    path = parsed.path or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))

def normalize_name(value: str) -> str:
    return " ".join(value.strip().split()).lower()
