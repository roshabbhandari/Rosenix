def take(values, count):
    if count < 0:
        raise ValueError("count must be non-negative")
    return list(values)[:count]
