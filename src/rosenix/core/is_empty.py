def is_empty(value):
    try:
        return len(value) == 0
    except TypeError:
        return value is None
