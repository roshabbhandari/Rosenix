def within(value, lower, upper):
    if lower > upper:
        raise ValueError("lower bound must not exceed upper bound")
    return lower <= value <= upper
