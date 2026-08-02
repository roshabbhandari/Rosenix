"""Layer 3: Runtime.

Execution primitives shared by every application kit: an async event
bus for observability, a task-graph executor for workflows/agents, and
contextvars-based tracing. No AI-specific logic lives here either —
this layer would be equally at home in a non-AI async application.
"""

from rosenix.runtime.errors import (
    FrameworkError,
    ProviderError,
    ToolExecutionError,
)
from rosenix.runtime.events import Event, EventBus
from rosenix.runtime.executor import Executor, Task, TaskResult
from rosenix.runtime.tracing import Tracer, current_span

__all__ = [
    "EventBus",
    "Event",
    "Executor",
    "Task",
    "TaskResult",
    "Tracer",
    "current_span",
    "FrameworkError",
    "ProviderError",
    "ToolExecutionError",
]
