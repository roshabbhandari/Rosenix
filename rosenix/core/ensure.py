def ensure(condition, message="condition failed"):
    if not condition:
        raise ValueError(message)
    return condition
