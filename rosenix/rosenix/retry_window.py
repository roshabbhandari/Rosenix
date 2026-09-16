def retry_allowed(attempt, limit):
    if limit < 0:
        raise ValueError("limit must not be negative")
    return 0 <= attempt < limit
