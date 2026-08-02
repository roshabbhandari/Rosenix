"""Layer 2: Provider Protocols.

Structural typing contracts (`typing.Protocol`), not abstract base
classes. Any object satisfying the shape works as a provider — no
inheritance, no framework coupling, no vendor lock-in. This is the
layer that guarantees a user's own class works without importing
anything from this framework except the type it's checked against.
"""

from rosenix.protocols.embedding import EmbeddingProvider
from rosenix.protocols.llm import Chunk, Completion, LLMProvider, Message
from rosenix.protocols.memory import Memory
from rosenix.protocols.tool import Tool, ToolSpec
from rosenix.protocols.vectorstore import VectorRecord, VectorStore

__all__ = [
    "LLMProvider",
    "Message",
    "Completion",
    "Chunk",
    "EmbeddingProvider",
    "VectorStore",
    "VectorRecord",
    "Tool",
    "ToolSpec",
    "Memory",
]
