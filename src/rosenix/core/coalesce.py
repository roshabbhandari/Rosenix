def coalesce(*values):
    for value in values:
        if value is not None:
            return value
    return None
