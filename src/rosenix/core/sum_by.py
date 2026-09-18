def sum_by(items, selector):
    return sum(selector(item) for item in items)
