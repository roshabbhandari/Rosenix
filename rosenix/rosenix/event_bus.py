from collections import defaultdict


class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, event, handler):
        self._handlers[event].append(handler)
        return handler

    def publish(self, event, payload=None):
        return [handler(payload) for handler in tuple(self._handlers.get(event, ()))]
