def clamp(value, minimum, maximum):
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    return max(minimum, min(value, maximum))
