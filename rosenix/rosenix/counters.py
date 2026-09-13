def count_by(items, key):
    counts = {}
    for item in items:
        value = key(item)
        counts[value] = counts.get(value, 0) + 1
    return counts
