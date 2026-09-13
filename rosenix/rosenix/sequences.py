def pairwise(items):
    values = list(items)
    return list(zip(values, values[1:]))


def sliding_window(items, size):
    if size <= 0:
        raise ValueError("size must be positive")
    values = list(items)
    return [values[i:i + size] for i in range(len(values) - size + 1)]
