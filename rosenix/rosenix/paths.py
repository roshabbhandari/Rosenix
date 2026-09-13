from pathlib import Path


def normalize_path(value):
    return Path(value).expanduser()


def ensure_suffix(path, suffix):
    value = Path(path)
    return value if value.suffix == suffix else value.with_suffix(suffix)
