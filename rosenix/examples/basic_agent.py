"""End-to-end example wiring all four layers together.

Run with:
    python examples/basic_agent.py

Uses `EchoProvider` (Layer 2 provider, zero network/dependencies) so
this runs anywhere with no API key required. Swap in
`rosenix.providers.openai_provider.OpenAIProvider` for a real model.
"""

import asyncio

from rosenix.kernel.container import Container, Lifetime
from rosenix.kernel.lifecycle import Lifecycle
from rosenix.kits.agent import Agent
from rosenix.providers.local_provider import EchoProvider
from rosenix.runtime.events import Event, EventBus


async def main() -> None:
    # --- Layer 1: kernel -------------------------------------------------
    container = Container()
    container.register(EchoProvider, lifetime=Lifetime.SINGLETON)

    lifecycle = Lifecycle()

    @lifecycle.on_startup
    async def announce_startup() -> None:
        print("[lifecycle] starting up")

    @lifecycle.on_shutdown
    async def announce_shutdown() -> None:
        print("[lifecycle] shutting down")

    # --- Layer 3: runtime (event bus for observability) -------------------
    events = EventBus()

    @events.on("agent.completion")
    async def log_completion(event: Event) -> None:
        print(f"[event] {event.name}: {event.payload['content']!r}")

    # --- Layer 2: provider, resolved from the container -------------------
    llm = container.resolve(EchoProvider)

    # --- Layer 4: the user-facing Agent kit --------------------------------
    agent = Agent(
        llm=llm,
        name="demo-agent",
        system_prompt="You are a terse, helpful assistant.",
        events=events,
    )

    async with lifecycle:
        reply = await agent.run("What's the capital of France?")
        print(f"\nFinal reply: {reply}")


if __name__ == "__main__":
    asyncio.run(main())
