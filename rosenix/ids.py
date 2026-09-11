from uuid import uuid4

def new_id(prefix: str = "") -> str:
    value = uuid4().hex
    return f"{prefix}_{value}" if prefix else value
