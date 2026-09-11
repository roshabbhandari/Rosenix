from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class Project:
    name: str
    path: Path

    def exists(self) -> bool:
        return self.path.is_dir()
