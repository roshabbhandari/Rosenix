from urllib.parse import urlparse


def is_absolute_url(value):
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def hostname(value):
    return urlparse(value).hostname
