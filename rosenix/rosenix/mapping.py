def map_values(mapping, function):
    return {key: function(value) for key, value in mapping.items()}


def filter_values(mapping, predicate):
    return {key: value for key, value in mapping.items() if predicate(value)}
