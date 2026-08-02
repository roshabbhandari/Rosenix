"""Framework exception hierarchy.

All framework-raised exceptions derive from `FrameworkError`, so
application code can catch broadly (`except FrameworkError`) or
narrowly (`except ToolExecutionError`) as needed. Nothing raises a bare
`Exception` from within the framework.
"""

from __future__ import annotations


class FrameworkError(Exception):
    """Base class for all errors raised by rosenix."""


class ProviderError(FrameworkError):
    """A provider (LLM, embedding, vector store, ...) failed."""

    def __init__(self, provider: str, message: str, *, cause: Exception | None = None) -> None:
        super().__init__(f"[{provider}] {message}")
        self.provider = provider
        self.__cause__ = cause


class ToolExecutionError(FrameworkError):
    """A tool call raised an exception during execution."""

    def __init__(self, tool_name: str, message: str, *, cause: Exception | None = None) -> None:
        super().__init__(f"Tool '{tool_name}' failed: {message}")
        self.tool_name = tool_name
        self.__cause__ = cause


class TaskCancelledError(FrameworkError):
    """A task graph node was cancelled before completion."""


class TaskFailedError(FrameworkError):
    """A task graph node raised during execution and no retries remain."""

    def __init__(self, task_id: str, message: str, *, cause: Exception | None = None) -> None:
        super().__init__(f"Task '{task_id}' failed: {message}")
        self.task_id = task_id
        self.__cause__ = cause
