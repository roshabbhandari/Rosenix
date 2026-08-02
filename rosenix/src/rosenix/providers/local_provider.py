"""Local provider.

Two things live here:

- `EchoProvider`: a zero-dependency, deterministic provider useful for
  tests and examples — no network calls, no API keys.
- `OllamaProvider`: a thin adapter over a local Ollama server, for
  running real open-weight models without any cloud dependency.

Both satisfy `LLMProvider` structurally.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from urllib import error as urllib_error
from urllib import request as urllib_request

from rosenix.protocols.llm import Chunk, Completion, Message, Usage
from rosenix.runtime.errors import ProviderError


class EchoProvider:
    """Deterministic no-network provider: echoes the last user message.

    Useful for unit tests and examples where a real model would be
    slow, costly, or non-deterministic.
    """

    def __init__(self, model: str = "echo-1") -> None:
        self.model = model

    async def complete(self, messages: list[Message], **kwargs: object) -> Completion:
        last_user = next((m for m in reversed(messages) if m.role == "user"), None)
        content = f"echo: {last_user.content}" if last_user else "echo: (no user message)"
        return Completion(
            content=content,
            model=self.model,
            usage=Usage(prompt_tokens=0, completion_tokens=0),
        )

    async def stream(self, messages: list[Message], **kwargs: object) -> AsyncIterator[Chunk]:
        completion = await self.complete(messages, **kwargs)
        for word in completion.content.split(" "):
            yield Chunk(delta=word + " ", model=self.model)


class OllamaProvider:
    """Adapter over a local Ollama server's `/api/chat` endpoint.

    Requires an Ollama server already running (default
    http://localhost:11434) with the target model pulled.
    """

    def __init__(self, model: str = "llama3", *, host: str = "http://localhost:11434") -> None:
        self.model = model
        self._host = host.rstrip("/")

    async def complete(self, messages: list[Message], **kwargs: object) -> Completion:
        payload = {
            "model": self.model,
            "messages": [m.model_dump(exclude_none=True) for m in messages],
            "stream": False,
        }
        payload.update(kwargs)
        data = await asyncio.to_thread(self._post, "/api/chat", payload)
        return Completion(
            content=data.get("message", {}).get("content", ""),
            model=self.model,
            usage=Usage(
                prompt_tokens=data.get("prompt_eval_count", 0),
                completion_tokens=data.get("eval_count", 0),
            ),
            raw=data,
        )

    async def stream(self, messages: list[Message], **kwargs: object) -> AsyncIterator[Chunk]:
        # Ollama supports streaming NDJSON; kept simple here via a single
        # non-streamed call (offloaded to a thread so it doesn't block the
        # event loop) split into word-chunks. Swap in an async HTTP client
        # (e.g. httpx) for real token-by-token streaming.
        completion = await self.complete(messages, **kwargs)
        for word in completion.content.split(" "):
            yield Chunk(delta=word + " ", model=self.model)

    def _post(self, path: str, payload: dict) -> dict:
        req = urllib_request.Request(
            f"{self._host}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib_request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib_error.URLError as exc:
            raise ProviderError(
                "ollama", f"could not reach Ollama at {self._host}: {exc}", cause=exc
            ) from exc
