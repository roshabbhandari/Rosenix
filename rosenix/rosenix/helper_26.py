def coalesce(*values):
    return next((value for value in values if value is not None), None)
