"""Agent.

A thin composition of an `LLMProvider`, optional `Memory`, and optional
`Tool`s. Deliberately has no hidden prompt templates: the system prompt
is a plain string you pass in, tool-calling is a visible loop you can
read top to bottom, and every step emits an event for observability.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rosenix.protocols.llm import LLMProvider, Message
from rosenix.protocols.memory import Memory
from rosenix.protocols.tool import Tool
from rosenix.runtime.errors import ToolExecutionError
from rosenix.runtime.events import Event, EventBus
from rosenix.runtime.tracing import Tracer


class _InMemoryHistory:
    """Default `Memory` implementation: a plain list, nothing persisted.

    Swap in a real `Memory` implementation (Redis, a database, ...) for
    anything beyond a single process's lifetime.
    """

    def __init__(self) -> None:
        self._messages: list[Message] = []

    async def append(self, message: Message) -> None:
        self._messages.append(message)

    async def history(self) -> list[Message]:
        return list(self._messages)

    async def clear(self) -> None:
        self._messages.clear()


@dataclass
class Agent:
    """A single LLM-backed agent with optional memory and tools.

    Example:
        agent = Agent(llm=my_provider, system_prompt="You are terse.")
        reply = await agent.run("What's 2+2?")
    """

    llm: LLMProvider
    system_prompt: str | None = None
    memory: Memory = field(default_factory=_InMemoryHistory)
    tools: list[Tool] = field(default_factory=list)
    name: str = "agent"
    max_tool_iterations: int = 5
    events: EventBus = field(default_factory=EventBus)
    tracer: Tracer = field(default_factory=Tracer)

    async def run(self, user_input: str) -> str:
        """Send `user_input`, run any resulting tool calls, return the
        final assistant text.
        """
        with self.tracer.span("agent.run", agent=self.name):
            if self.system_prompt and not await self.memory.history():
                await self.memory.append(Message(role="system", content=self.system_prompt))

            await self.memory.append(Message(role="user", content=user_input))
            await self.events.publish(
                Event("agent.user_message", {"agent": self.name, "content": user_input})
            )

            for _ in range(self.max_tool_iterations):
                history = await self.memory.history()
                completion = await self.llm.complete(history)
                await self.events.publish(
                    Event("agent.completion", {"agent": self.name, "content": completion.content})
                )

                await self.memory.append(Message(role="assistant", content=completion.content))

                tool_call = self._extract_tool_call(completion.content)
                if tool_call is None:
                    return completion.content

                tool_name, tool_args = tool_call
                result = await self._call_tool(tool_name, tool_args)
                await self.memory.append(
                    Message(role="tool", content=str(result), name=tool_name)
                )

            return "Reached max tool iterations without a final answer."

    async def _call_tool(self, name: str, kwargs: dict) -> object:
        tool = next((t for t in self.tools if t.spec.name == name), None)
        if tool is None:
            raise ToolExecutionError(name, "no such tool registered")

        with self.tracer.span("agent.tool_call", tool=name):
            await self.events.publish(
                Event("agent.tool_call", {"agent": self.name, "tool": name, "args": kwargs})
            )
            try:
                return await tool(**kwargs)
            except Exception as exc:  # noqa: BLE001 - re-raised as a typed framework error
                raise ToolExecutionError(name, str(exc), cause=exc) from exc

    @staticmethod
    def _extract_tool_call(content: str) -> tuple[str, dict] | None:
        """Placeholder tool-call detection.

        Real providers return structured tool-call fields on `Completion`
        rather than encoding calls in text; this stays intentionally
        simple and explicit so the control flow above is easy to follow.
        Replace with your provider's structured tool-call parsing.
        """
        return None
