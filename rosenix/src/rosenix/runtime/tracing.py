"""Contextvars-based tracing.

Spans nest via `contextvars`, so tracing works correctly across
`await` points and concurrent tasks without manually threading a
context object through every function call. Designed to be OpenTelemetry
-compatible: `Tracer` can optionally forward spans to an OTel exporter
if the `otel` optional dependency is installed, but has zero required
dependency on it.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

_current_span: ContextVar[Span | None] = ContextVar("_current_span", default=None)


@dataclass
class Span:
    """A single traced operation, possibly nested inside a parent span."""

    name: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_id: str | None = None
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float | None:
        if self.end_time is None:
            return None
        return self.end_time - self.start_time


def current_span() -> Span | None:
    """Return the span currently active in this context, if any."""
    return _current_span.get()


class Tracer:
    """Creates and records spans; optionally forwards them to OTel.

    Example:
        tracer = Tracer()

        with tracer.span("agent.run", agent="researcher") as span:
            span.attributes["result_length"] = 42
        # span recorded to tracer.finished_spans on exit
    """

    def __init__(self, *, otel_tracer: Any | None = None) -> None:
        self._otel_tracer = otel_tracer
        self.finished_spans: list[Span] = []

    @contextmanager
    def span(self, name: str, **attributes: Any) -> Iterator[Span]:
        parent = current_span()
        span = Span(name=name, parent_id=parent.span_id if parent else None, attributes=dict(attributes))
        token = _current_span.set(span)

        otel_ctx = None
        if self._otel_tracer is not None:
            otel_ctx = self._otel_tracer.start_as_current_span(name)
            otel_ctx.__enter__()

        try:
            yield span
        finally:
            span.end_time = time.time()
            self.finished_spans.append(span)
            _current_span.reset(token)
            if otel_ctx is not None:
                otel_ctx.__exit__(None, None, None)
