def sequence_ids(count, start=1):
    if count < 0:
        raise ValueError("count must not be negative")
    return list(range(start, start + count))
