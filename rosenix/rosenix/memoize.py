from functools import lru_cache


def memoized(maxsize=128):
    if maxsize is not None and maxsize < 1:
        raise ValueError("maxsize must be positive or None")

    def decorate(function):
        return lru_cache(maxsize=maxsize)(function)

    return decorate
