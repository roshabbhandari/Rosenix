"""Layered, typed configuration.

Precedence (lowest to highest): defaults -> file -> environment variables
-> explicit overrides passed in code. Later layers win. Config is a
plain Pydantic model, so it's fully typed, validated, and serializable —
no untyped dict-of-dicts passed around the framework.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Generic, Self, TypeVar

from pydantic import BaseModel

ConfigT = TypeVar("ConfigT", bound=BaseModel)


class Config(Generic[ConfigT]):
    """Builds a validated config object from layered sources.

    `Config` is generic over the schema passed to `__init__`, so
    `build()`'s return type is the *actual* schema type given —
    `Config(AppConfig).build()` is statically known to return `AppConfig`,
    not a bare `BaseModel`.

    Example:
        class AppConfig(BaseModel):
            model: str = "gpt-4o-mini"
            temperature: float = 0.7
            max_retries: int = 3

        config: AppConfig = (
            Config(AppConfig)
            .from_file("config.json")        # optional, ignored if missing
            .from_env(prefix="ROSENIX_")     # ROSENIX_MODEL, etc.
            .with_overrides(temperature=0.2)  # explicit, wins over all
            .build()
        )
    """

    def __init__(self, schema: type[ConfigT]) -> None:
        self._schema = schema
        self._layers: dict[str, Any] = {}

    def from_file(self, path: str | Path) -> Self:
        p = Path(path)
        if p.exists():
            self._layers.update(json.loads(p.read_text()))
        return self

    def from_env(self, prefix: str = "") -> Self:
        fields = self._schema.model_fields
        for name in fields:
            env_key = f"{prefix}{name}".upper()
            if env_key in os.environ:
                self._layers[name] = os.environ[env_key]
        return self

    def with_overrides(self, **overrides: Any) -> Self:
        self._layers.update(overrides)
        return self

    def build(self) -> ConfigT:
        """Validate accumulated layers against the schema and return it."""
        return self._schema.model_validate(self._layers)
