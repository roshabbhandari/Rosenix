def last(values, default=None):
    found = False
    result = default
    for value in values:
        found = True
        result = value
    return result if found else default
