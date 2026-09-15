def normalize_text(value):
    if not isinstance(value, str):
        raise TypeError("value must be text")
    return " ".join(value.split())


def safe_lower(value):
    return normalize_text(value).casefold()
