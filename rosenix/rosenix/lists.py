def first(items, default=None):
    for item in items:
        return item
    return default


def last(items, default=None):
    found = default
    for item in items:
        found = item
    return found
