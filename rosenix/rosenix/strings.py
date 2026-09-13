def truncate(text, limit, suffix="..."):
    if limit < 0:
        raise ValueError("limit must be non-negative")
    if len(text) <= limit:
        return text
    if len(suffix) >= limit:
        return suffix[:limit]
    return text[:limit - len(suffix)] + suffix
