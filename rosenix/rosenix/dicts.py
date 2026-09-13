def without_none(mapping):
    return {key: value for key, value in mapping.items() if value is not None}


def merge_dicts(left, right):
    result = dict(left)
    result.update(right)
    return result
