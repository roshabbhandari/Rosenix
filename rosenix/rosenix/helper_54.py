def intersection(left, right):
    right = set(right)
    return [value for value in left if value in right]
