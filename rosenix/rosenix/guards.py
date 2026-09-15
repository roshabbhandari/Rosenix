def ensure(condition, message="condition failed"):
    if not condition:
        raise ValueError(message)
    return True


def ensure_type(value, expected, name="value"):
    if not isinstance(value, expected):
        raise TypeError(f"{name} must be {expected}")
    return value
