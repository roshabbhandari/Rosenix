def exponential_delay(attempt: int, base: float = 0.5, maximum: float = 30.0) -> float:
    if attempt < 0:
        raise ValueError("attempt must be non-negative")
    return min(maximum, base * (2 ** attempt))

def linear_delay(attempt: int, base: float = 0.5, maximum: float = 30.0) -> float:
    if attempt < 0:
        raise ValueError("attempt must be non-negative")
    return min(maximum, base * (attempt + 1))
