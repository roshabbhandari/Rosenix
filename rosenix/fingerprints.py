import hashlib
from typing import Any
from .serialization import dumps

def fingerprint(value: Any, algorithm: str = "sha256") -> str:
    data = dumps(value).encode("utf-8")
    digest = hashlib.new(algorithm)
    digest.update(data)
    return digest.hexdigest()
