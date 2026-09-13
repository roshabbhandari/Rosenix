import json


def dumps_compact(value):
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def loads_object(value):
    result = json.loads(value)
    if not isinstance(result, dict):
        raise ValueError("JSON value must be an object")
    return result
