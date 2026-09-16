def partition(items, predicate):
    matched = []
    rejected = []
    for item in items:
        (matched if predicate(item) else rejected).append(item)
    return matched, rejected
