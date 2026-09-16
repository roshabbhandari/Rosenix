def safe_index(values, index, default=None):
    try:
        return values[index]
    except (IndexError, KeyError):
        return default
