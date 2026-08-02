# Rosenix

[![CI](https://github.com/rosenix-project/rosenix/actions/workflows/ci.yml/badge.svg)](https://github.com/rosenix-project/rosenix/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modular, explicit, non-magical framework for building AI-powered software
systems: assistants, agents, multi-agent systems, AI APIs, workflows, and
more — on one consistent architecture.

## Philosophy

- **Nothing is magical, nothing is hidden.** No implicit prompt templates,
  no hidden chains. Every behavior is a plain, typed, inspectable object.
- **Composition over inheritance.** Providers are `typing.Protocol`s, not
  base classes — any object with the right shape works, no framework
  coupling required.
- **Everything is a plugin.** LLMs, embeddings, vector stores, tools, and
  memory backends all register through the same plugin system, including
  third-party packages via `entry_points`.

## Architecture (4 layers)

```
Layer 4  kits/       Agent, Workflow, Tool decorator      (opinionated)
Layer 3  runtime/     event bus, task executor, tracing    (execution)
Layer 2  protocols/   LLMProvider, EmbeddingProvider, ...   (contracts)
Layer 1  kernel/      DI container, plugin registry, config (foundation)
```

Each layer only depends on the layers below it. Layer 1 has zero
AI-specific code — it's a generic application kernel, on purpose, so the
architecture is proven before AI complexity is added.

## Quickstart

```bash
pip install -e ".[dev,openai]"
```

```python
import asyncio
from rosenix.kernel.container import Container
from rosenix.providers.openai_provider import OpenAIProvider
from rosenix.kits.agent import Agent

async def main():
    container = Container()
    container.register(OpenAIProvider, lambda: OpenAIProvider(model="gpt-4o-mini"))

    agent = Agent(llm=container.resolve(OpenAIProvider), name="assistant")
    reply = await agent.run("Say hello in one sentence.")
    print(reply)

asyncio.run(main())
```

See `examples/basic_agent.py` for a full runnable example.

## Development

```bash
pip install -e ".[dev,openai]"
pytest --cov=rosenix --cov-report=term-missing
mypy src/rosenix
ruff check src/ tests/ examples/
```

See `CONTRIBUTING.md` for local setup details and current test-coverage
gaps that are good first contributions.

## Project status

Pre-alpha (`0.x`). The architecture is stable; test coverage on
`kits/` and `providers/` is still being built out — see `ROADMAP.md`.
Not yet recommended for production use.
