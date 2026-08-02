"""Workflow.

A friendlier, decorator-based builder over `runtime.executor.Executor`,
for defining multi-step pipelines (of agents, tools, or plain functions)
as a readable sequence rather than manual `Task` construction.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from rosenix.runtime.executor import Executor, Task, TaskResult


@dataclass
class Workflow:
    """Declarative multi-step pipeline builder.

    Example:
        workflow = Workflow(name="research_pipeline")

        @workflow.step("search")
        async def search() -> list[str]:
            return ["result a", "result b"]

        @workflow.step("summarize", depends_on=["search"])
        async def summarize() -> str:
            return "summary"

        results = await workflow.run()
        results["summarize"].value
    """

    name: str
    _executor: Executor = field(default_factory=Executor, repr=False)

    def step(
        self, task_id: str, *, depends_on: list[str] | None = None, max_retries: int = 0
    ) -> Callable[[Callable[[], Awaitable[Any]]], Callable[[], Awaitable[Any]]]:
        def decorator(func: Callable[[], Awaitable[Any]]) -> Callable[[], Awaitable[Any]]:
            self._executor.add(
                Task(
                    id=task_id,
                    action=func,
                    depends_on=tuple(depends_on or ()),
                    max_retries=max_retries,
                )
            )
            return func

        return decorator

    async def run(self, *, stop_on_failure: bool = True) -> dict[str, TaskResult]:
        return await self._executor.run(stop_on_failure=stop_on_failure)
