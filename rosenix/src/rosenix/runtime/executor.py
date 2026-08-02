"""Task graph executor.

Workflows and multi-step agents are expressed as a DAG of `Task`s with
explicit dependencies. The executor runs independent tasks concurrently,
respects ordering where dependencies exist, retries failed tasks with
backoff, and propagates cancellation to still-pending tasks if any
required task fails permanently — structured-concurrency style, so a
failure can't leave orphaned background work running.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Generic, Self, TypeVar

from rosenix.runtime.errors import TaskCancelledError, TaskFailedError

T = TypeVar("T")

Action = Callable[..., Awaitable[T]]


@dataclass
class Task(Generic[T]):
    """A single node in the task graph.

    `depends_on` names other tasks (by id) that must complete first;
    their results are *not* auto-passed in — read them from
    `TaskResult.value` via the executor's results dict inside `action`
    if needed, keeping data flow explicit rather than implicit.
    """

    id: str
    action: Action
    depends_on: tuple[str, ...] = ()
    max_retries: int = 0
    retry_backoff_seconds: float = 0.5


@dataclass
class TaskResult(Generic[T]):
    task_id: str
    value: T | None = None
    error: Exception | None = None
    attempts: int = 0

    @property
    def succeeded(self) -> bool:
        return self.error is None


@dataclass
class _Node:
    task: Task
    result: TaskResult | None = None
    future: asyncio.Future[TaskResult] | None = None


class Executor:
    """Runs a set of `Task`s honoring dependency order and concurrency.

    Example:
        executor = Executor()
        executor.add(Task(id="fetch", action=fetch_data))
        executor.add(Task(id="summarize", action=summarize, depends_on=("fetch",)))
        results = await executor.run()
        results["summarize"].value
    """

    def __init__(self) -> None:
        self._nodes: dict[str, _Node] = {}

    def add(self, task: Task) -> Self:
        self._nodes[task.id] = _Node(task=task)
        return self

    async def run(self, *, stop_on_failure: bool = True) -> dict[str, TaskResult]:
        """Execute all tasks, respecting dependency order.

        If `stop_on_failure` is True (default), any task whose
        dependency failed is recorded as cancelled rather than run.
        """
        self._validate_no_cycles()

        async with asyncio.TaskGroup() as tg:
            for node in self._nodes.values():
                node.future = tg.create_task(self._run_node(node, stop_on_failure))

        return {task_id: node.result for task_id, node in self._nodes.items() if node.result}

    async def _run_node(self, node: _Node, stop_on_failure: bool) -> TaskResult:
        for dep_id in node.task.depends_on:
            dep = self._nodes[dep_id]
            assert dep.future is not None
            dep_result = await dep.future
            if stop_on_failure and not dep_result.succeeded:
                cancelled_result: TaskResult[Any] = TaskResult(
                    task_id=node.task.id,
                    error=TaskCancelledError(
                        f"'{node.task.id}' cancelled: dependency '{dep_id}' failed"
                    ),
                )
                node.result = cancelled_result
                return cancelled_result

        result = await self._run_with_retries(node.task)
        node.result = result
        return result

    async def _run_with_retries(self, task: Task) -> TaskResult:
        attempts = 0
        last_error: Exception | None = None
        while attempts <= task.max_retries:
            attempts += 1
            try:
                value = await task.action()
                return TaskResult(task_id=task.id, value=value, attempts=attempts)
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 - retried and reported, not swallowed
                last_error = exc
                if attempts <= task.max_retries:
                    await asyncio.sleep(task.retry_backoff_seconds * attempts)

        return TaskResult(
            task_id=task.id,
            error=TaskFailedError(task.id, str(last_error), cause=last_error),
            attempts=attempts,
        )

    def _validate_no_cycles(self) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(task_id: str, path: list[str]) -> None:
            if task_id in visited:
                return
            if task_id in visiting:
                cycle = " -> ".join(path + [task_id])
                raise ValueError(f"Cycle detected in task graph: {cycle}")
            visiting.add(task_id)
            for dep in self._nodes[task_id].task.depends_on:
                visit(dep, path + [task_id])
            visiting.discard(task_id)
            visited.add(task_id)

        for task_id in self._nodes:
            visit(task_id, [])
