"""OpenAI provider.

Satisfies `LLMProvider` structurally — no base class from this
framework is inherited. Requires the `openai` extra:
    pip install "rosenix[openai]"
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from rosenix.protocols.llm import Chunk, Completion, Message, Usage
from rosenix.runtime.errors import ProviderError


class OpenAIProvider:
    """Thin adapter over the OpenAI chat-completions API."""

    def __init__(self, model: str = "gpt-4o-mini", *, api_key: str | None = None) -> None:
        self.model = model
        self._api_key = api_key
        self._client = None  # lazily constructed, see _get_client

    def _get_client(self):
        if self._client is None:
            try:
                from openai import AsyncOpenAI
            except ImportError as exc:
                raise ProviderError(
                    "openai", "the 'openai' package is required; install with pip install 'rosenix[openai]'"
                ) from exc
            self._client = AsyncOpenAI(api_key=self._api_key)
        return self._client

    async def complete(self, messages: list[Message], **kwargs: object) -> Completion:
        client = self._get_client()
        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[m.model_dump(exclude_none=True) for m in messages],
                **kwargs,
            )
        except Exception as exc:  # noqa: BLE001 - normalized into ProviderError
            raise ProviderError("openai", str(exc), cause=exc) from exc

        choice = response.choices[0]
        return Completion(
            content=choice.message.content or "",
            model=response.model,
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
                completion_tokens=response.usage.completion_tokens if response.usage else 0,
            ),
            finish_reason=choice.finish_reason,
            raw=response.model_dump(),
        )

    async def stream(self, messages: list[Message], **kwargs: object) -> AsyncIterator[Chunk]:
        client = self._get_client()
        try:
            stream = await client.chat.completions.create(
                model=self.model,
                messages=[m.model_dump(exclude_none=True) for m in messages],
                stream=True,
                **kwargs,
            )
            async for event in stream:
                delta = event.choices[0].delta.content or ""
                yield Chunk(
                    delta=delta,
                    model=event.model,
                    finish_reason=event.choices[0].finish_reason,
                )
        except Exception as exc:  # noqa: BLE001 - normalized into ProviderError
            raise ProviderError("openai", str(exc), cause=exc) from exc
