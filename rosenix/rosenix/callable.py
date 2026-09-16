def is_callable(value):
    return callable(value)


def call_if_callable(value, *args, **kwargs):
    return value(*args, **kwargs) if callable(value) else value
