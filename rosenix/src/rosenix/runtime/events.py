"""Async event bus.

Every meaningful framework action (agent step, tool call, LLM request)
emits an event here. This is how observability, logging, and metrics
attach without hardcoding a logging call into every internal function —
subscribers decide what to do with events, the framework just emits.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

Handler = Callable[["Event"], Awaitable[None] | None]


@dataclass(frozen=True)
class Event:
    """A single occurrence published to the bus."""

    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class EventBus:
    """A minimal async pub/sub bus.

    Example:
        bus = EventBus()

        @bus.on("agent.step")
        async def log_step(event: Event) -> None:
            print(event.payload)

        await bus.publish(Event("agent.step", {"agent": "researcher"}))

    Handlers may be sync or async. Wildcard subscription (`"*"`) receives
    every event regardless of name — useful for a single tracing/logging
    subscriber that mirrors everything.
    """

    WILDCARD = "*"

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = {}

    def on(self, name: str) -> Callable[[Handler], Handler]:
        """Decorator form: subscribe a handler to events named `name`."""

        def decorator(handler: Handler) -> Handler:
            self.subscribe(name, handler)
            return handler

        return decorator

    def subscribe(self, name: str, handler: Handler) -> None:
        self._handlers.setdefault(name, []).append(handler)

    def unsubscribe(self, name: str, handler: Handler) -> None:
        handlers = self._handlers.get(name, [])
        if handler in handlers:
            handlers.remove(handler)

    async def publish(self, event: Event) -> None:
        """Notify every handler subscribed to `event.name` plus wildcards.

        Handlers run concurrently; an exception in one handler does not
        prevent others from running, but is re-raised (grouped) after
        all handlers complete, so subscriber bugs are visible instead of
        silently swallowed.
        """
        handlers = self._handlers.get(event.name, []) + self._handlers.get(self.WILDCARD, [])
        if not handlers:
            return

        async def run(handler: Handler) -> None:
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result

        results = await asyncio.gather(*(run(h) for h in handlers), return_exceptions=True)
        errors = [r for r in results if isinstance(r, Exception)]
        if errors:
            raise ExceptionGroup(f"error(s) handling event '{event.name}'", errors)
