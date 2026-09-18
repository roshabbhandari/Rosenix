def cache_key(*parts):
    return "|".join(str(part) for part in parts)
