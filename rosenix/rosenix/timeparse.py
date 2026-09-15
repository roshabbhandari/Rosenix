def seconds(value):
    if isinstance(value, bool):
        raise TypeError("boolean is not a duration")
    if isinstance(value, (int, float)):
        if value < 0:
            raise ValueError("duration must be non-negative")
        return float(value)
    raise TypeError("duration must be numeric")
