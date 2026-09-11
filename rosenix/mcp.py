from dataclasses import dataclass, field

@dataclass(slots=True)
class MCPServer:
    name: str
    command: list[str] = field(default_factory=list)
    enabled: bool = True

class MCPRegistry:
    def __init__(self):
        self.servers: dict[str, MCPServer] = {}

    def add(self, server: MCPServer) -> None:
        self.servers[server.name] = server

    def remove(self, name: str) -> None:
        self.servers.pop(name, None)
