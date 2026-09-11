from .messages import Message

class ContextWindow:
    def __init__(self, limit: int = 20):
        self.limit = max(1, limit)
        self.messages: list[Message] = []

    def add(self, message: Message) -> None:
        self.messages.append(message)
        self.messages = self.messages[-self.limit:]

    def export(self) -> list[dict[str, str]]:
        return [message.as_dict() for message in self.messages]
