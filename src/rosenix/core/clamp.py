def clamp(value, minimum, maximum):
    if minimum > maximum:
        raise ValueError("minimum cannot exceed maximum")
    return max(minimum, min(value, maximum))
