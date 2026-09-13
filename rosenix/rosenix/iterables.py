def first(items, default=None):
    for item in items:
        return item
    return default


def unique(items):
    return list(dict.fromkeys(items))
