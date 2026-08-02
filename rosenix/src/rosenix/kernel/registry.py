"""Plugin registry.

Discovers and loads third-party providers via Python packaging
``entry_points``, so `pip install rosenix-openai` is enough to make
a provider available — no manual import or config wiring required.

A plugin package declares itself in its own `pyproject.toml`:

    [project.entry-points."rosenix.providers"]
    openai = "rosenix_openai:OpenAIProvider"

`Registry.discover()` then finds it without rosenix needing to know
the plugin package exists ahead of time.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from importlib.metadata import entry_points
from typing import Any

DEFAULT_GROUP = "rosenix.providers"


@dataclass
class PluginInfo:
    name: str
    group: str
    loader: Callable[[], Any]
    _loaded: Any | None = field(default=None, repr=False)

    def load(self) -> Any:
        if self._loaded is None:
            self._loaded = self.loader()
        return self._loaded


class Registry:
    """In-process registry of named plugins, with lazy loading.

    Plugins are only imported when `.load()` is called on them, so
    discovering 50 installed providers doesn't pay the import cost of
    all 50 at startup — only the ones actually used.
    """

    def __init__(self) -> None:
        self._plugins: dict[str, dict[str, PluginInfo]] = {}

    def register(self, name: str, loader: Callable[[], Any], *, group: str = DEFAULT_GROUP) -> None:
        """Manually register a plugin (for local/in-repo providers)."""
        self._plugins.setdefault(group, {})[name] = PluginInfo(name=name, group=group, loader=loader)

    def discover(self, *, group: str = DEFAULT_GROUP) -> None:
        """Scan installed packages' entry_points for the given group and
        register any found, without importing them yet.
        """
        self._plugins.setdefault(group, {})
        for ep in entry_points(group=group):
            self._plugins[group][ep.name] = PluginInfo(
                name=ep.name, group=group, loader=ep.load
            )

    def get(self, name: str, *, group: str = DEFAULT_GROUP) -> Any:
        """Load and return the plugin registered under `name`."""
        try:
            return self._plugins[group][name].load()
        except KeyError as exc:
            available = sorted(self._plugins.get(group, {}))
            raise KeyError(
                f"No plugin named '{name}' in group '{group}'. "
                f"Available: {available or '(none registered/discovered)'}"
            ) from exc

    def names(self, *, group: str = DEFAULT_GROUP) -> list[str]:
        return sorted(self._plugins.get(group, {}))

    def __iter__(self) -> Iterator[str]:
        yield from self._plugins
