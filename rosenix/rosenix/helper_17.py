def pairwise(values):
    values = list(values)
    return list(zip(values, values[1:]))
