from dataclasses import dataclass

@dataclass(frozen=True)
class Limits:
    max_context_items: int = 50
    max_tool_output_chars: int = 20000
    max_history_items: int = 100
    max_retries: int = 3

    def bounded(self, value: int, maximum: int) -> int:
        return max(0, min(value, maximum))
