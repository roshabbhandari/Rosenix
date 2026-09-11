from pathlib import Path

TEXT_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".cpp", ".h", ".md", ".json", ".toml"}

def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS

def list_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file()]
