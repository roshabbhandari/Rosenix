import time


def debounce_ready(last_run, interval, now=None):
    current = time.monotonic() if now is None else now
    return last_run is None or current - last_run >= interval
