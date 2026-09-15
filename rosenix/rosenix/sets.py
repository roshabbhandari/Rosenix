def unique(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def difference(left, right):
    blocked = set(right)
    return [item for item in left if item not in blocked]
