def batches(items, size):
    if size < 1:
        raise ValueError("size must be positive")
    values = list(items)
    for index in range(0, len(values), size):
        yield values[index:index + size]
