def has_duplicates(values):
    values = list(values)
    return len(values) != len(set(values))
