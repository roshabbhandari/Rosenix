def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def to_number(value, default=None):
    if is_number(value):
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
