import os


def get_env(name, default=None):
    value = os.getenv(name)
    return default if value is None else value


def has_env(name):
    return bool(os.getenv(name))
