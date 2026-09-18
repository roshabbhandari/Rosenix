def safe_get(mapping, key, default=None):
    if mapping is None:
        return default
    return mapping.get(key, default)
