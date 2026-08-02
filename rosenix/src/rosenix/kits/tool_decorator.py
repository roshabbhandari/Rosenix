"""`@tool` decorator.

Wraps a plain async function into an object satisfying the `Tool`
protocol, deriving its JSON-schema parameter spec from the function's
own type hints and docstring — no separate schema to keep in sync by
hand.
"""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import Any, get_type_hints

from rosenix.protocols.tool import ToolSpec

_TYPE_TO_JSON_SCHEMA: dict[type, dict[str, str]] = {
    str: {"type": "string"},
    int: {"type": "integer"},
    float: {"type": "number"},
    bool: {"type": "boolean"},
    list: {"type": "array"},
    dict: {"type": "object"},
}


class FunctionTool:
    """A `Tool`-protocol-satisfying wrapper around a plain function."""

    def __init__(
        self,
        func: Callable[..., Awaitable[Any]],
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        self._func = func
        self._spec = ToolSpec(
            name=name or func.__name__,
            description=description or (inspect.getdoc(func) or ""),
            parameters=self._build_schema(func),
        )

    @staticmethod
    def _build_schema(func: Callable[..., Any]) -> dict:
        hints = get_type_hints(func)
        sig = inspect.signature(func)
        properties: dict[str, Any] = {}
        required: list[str] = []

        for name, param in sig.parameters.items():
            annotation = hints.get(name, str)
            schema = _TYPE_TO_JSON_SCHEMA.get(annotation, {"type": "string"})
            properties[name] = schema
            if param.default is inspect.Parameter.empty:
                required.append(name)

        return {"type": "object", "properties": properties, "required": required}

    @property
    def spec(self) -> ToolSpec:
        return self._spec

    async def __call__(self, **kwargs: Any) -> Any:
        result = self._func(**kwargs)
        if inspect.isawaitable(result):
            return await result
        return result


def tool(
    func: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
) -> FunctionTool | Callable[[Callable[..., Any]], FunctionTool]:
    """Turn a function into a Tool. Usable bare or with arguments.

    Example:
        @tool
        async def get_weather(city: str) -> str:
            '''Look up the current weather for a city.'''
            return f"sunny in {city}"

        @tool(name="search", description="Search the web")
        async def web_search(query: str) -> list[str]:
            ...
    """

    def decorator(f: Callable[..., Any]) -> FunctionTool:
        return FunctionTool(f, name=name, description=description)

    if func is not None:
        return decorator(func)
    return decorator
