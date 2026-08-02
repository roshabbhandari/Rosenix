from collections.abc import AsyncIterator

from rosenix.protocols.llm import Chunk, Completion, LLMProvider, Message


class PlainClassNotImportingProtocol:
    """Deliberately does NOT import or inherit from LLMProvider, proving
    structural typing works without any coupling to this framework.
    """

    async def complete(self, messages: list[Message], **kwargs: object) -> Completion:
        return Completion(content="ok", model="fake-model")

    async def stream(self, messages: list[Message], **kwargs: object) -> AsyncIterator[Chunk]:
        yield Chunk(delta="ok", model="fake-model")


def test_structural_typing_isinstance_check_passes():
    provider = PlainClassNotImportingProtocol()
    assert isinstance(provider, LLMProvider)


async def test_plain_class_complete_works():
    provider = PlainClassNotImportingProtocol()
    result = await provider.complete([Message(role="user", content="hi")])
    assert result.content == "ok"


def test_incomplete_class_fails_isinstance_check():
    class MissingStream:
        async def complete(self, messages, **kwargs):
            return Completion(content="x", model="m")

    assert not isinstance(MissingStream(), LLMProvider)
