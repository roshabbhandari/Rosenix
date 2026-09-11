class PermissionPolicy:
    def __init__(self, allowed: set[str] | None = None):
        self.allowed = allowed or set()

    def can_use(self, tool_name: str) -> bool:
        return "*" in self.allowed or tool_name in self.allowed
