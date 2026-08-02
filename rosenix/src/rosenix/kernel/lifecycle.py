"""Application lifecycle: ordered async startup/shutdown hooks.

Providers, connection pools, and background tasks register hooks here
instead of doing work in `__init__`, so startup is explicit, ordered,
awaitable, and shutdown always runs (even on error) in reverse order —
the same pattern as an async context manager stack.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Self

Hook = Callable[[], Awaitable[None]]


class Lifecycle:
    """Registers and runs startup/shutdown hooks in a predictable order.

    Example:
        lifecycle = Lifecycle()
        lifecycle.on_startup(db.connect)
        lifecycle.on_shutdown(db.disconnect)

        async with lifecycle:
            ...  # app runs; db.connect() already awaited
        # db.disconnect() awaited on exit, even if an exception occurred
    """

    def __init__(self) -> None:
        self._startup_hooks: list[Hook] = []
        self._shutdown_hooks: list[Hook] = []
        self._started = False

    def on_startup(self, hook: Hook) -> Hook:
        """Register a hook to run on startup, in registration order.

        Can be used as a plain call or as a decorator:
            @lifecycle.on_startup
            async def connect(): ...
        """
        self._startup_hooks.append(hook)
        return hook

    def on_shutdown(self, hook: Hook) -> Hook:
        """Register a hook to run on shutdown, in *reverse* registration
        order (mirrors context-manager unwind semantics).
        """
        self._shutdown_hooks.append(hook)
        return hook

    async def startup(self) -> None:
        if self._started:
            return
        for hook in self._startup_hooks:
            await hook()
        self._started = True

    async def shutdown(self) -> None:
        if not self._started:
            return
        errors: list[Exception] = []
        for hook in reversed(self._shutdown_hooks):
            try:
                await hook()
            except Exception as exc:  # noqa: BLE001 - collect, don't abort unwind
                errors.append(exc)
        self._started = False
        if errors:
            raise ExceptionGroup("errors during shutdown", errors)

    async def __aenter__(self) -> Self:
        await self.startup()
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.shutdown()
