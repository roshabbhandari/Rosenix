def chunk(values, size):
    if size <= 0:
        raise ValueError("size must be positive")
    values = list(values)
    return [values[index:index + size] for index in range(0, len(values), size)]
