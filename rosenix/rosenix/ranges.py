def within(value, minimum, maximum, inclusive=True):
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    if inclusive:
        return minimum <= value <= maximum
    return minimum < value < maximum


def clamp_range(value, minimum, maximum):
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    return max(minimum, min(maximum, value))
