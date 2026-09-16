def priority_value(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def higher_priority(first, second):
    return priority_value(first) > priority_value(second)
