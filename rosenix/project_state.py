from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class ProjectState:
    root: Path
    metadata: dict[str, Any] = field(default_factory=dict)
    dirty: bool = False

    def mark_dirty(self) -> None:
        self.dirty = True

    def mark_clean(self) -> None:
        self.dirty = False
