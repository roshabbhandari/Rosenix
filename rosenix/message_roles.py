from enum import StrEnum

class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

    @property
    def model_visible(self) -> bool:
        return self is not self.TOOL
