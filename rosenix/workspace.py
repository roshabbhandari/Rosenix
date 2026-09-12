from pathlib import Path

class Workspace:
    def __init__(self, root: str | Path):
        self.root = Path(root).expanduser().resolve()

    def contains(self, path: str | Path) -> bool:
        candidate = Path(path).expanduser().resolve()
        try:
            candidate.relative_to(self.root)
            return True
        except ValueError:
            return False

    def resolve(self, path: str | Path) -> Path:
        candidate = (self.root / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
        if not self.contains(candidate):
            raise ValueError("path escapes workspace")
        return candidate
