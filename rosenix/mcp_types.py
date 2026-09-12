from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class MCPTool:
    name: str
    description: str = ""
    input_schema: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class MCPResource:
    uri: str
    name: str
    description: str = ""
