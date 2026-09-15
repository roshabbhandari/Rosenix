def invoke(callback, *args, **kwargs):
    if callback is None:
        return None
    if not callable(callback):
        raise TypeError("callback must be callable")
    return callback(*args, **kwargs)


def chain(*callbacks):
    active = [callback for callback in callbacks if callback is not None]

    def run(value):
        for callback in active:
            value = callback(value)
        return value

    return run
