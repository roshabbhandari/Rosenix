"""Dependency injection container.

Resolves dependencies by type, with explicit lifetimes (singleton,
transient, scoped) and automatic constructor-argument resolution via
type hints. No decorators required on the classes being resolved —
registration is done at the container, not on the class itself, which
keeps the classes framework-agnostic.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Self, TypeVar, get_type_hints

T = TypeVar("T")

Factory = Callable[..., T]


class Lifetime(Enum):
    """How long a resolved instance should live."""

    SINGLETON = auto()  # one instance for the container's lifetime
    TRANSIENT = auto()  # a new instance every resolve()
    SCOPED = auto()  # one instance per active scope (see Container.scope())


class ContainerError(Exception):
    """Base error for all container-related failures."""


class UnregisteredDependencyError(ContainerError):
    """Raised when resolve() is asked for a type with no registration."""

    def __init__(self, key: type) -> None:
        super().__init__(
            f"No registration found for {key!r}. "
            f"Register it with container.register(...) before resolving."
        )
        self.key = key


class CircularDependencyError(ContainerError):
    """Raised when resolving a type would require resolving itself."""

    def __init__(self, chain: list[type]) -> None:
        path = " -> ".join(t.__name__ for t in chain)
        super().__init__(f"Circular dependency detected: {path}")
        self.chain = chain


@dataclass
class _Registration:
    factory: Factory
    lifetime: Lifetime
    instance: Any | None = field(default=None, repr=False)


class Container:
    """A small, explicit dependency-injection container.

    Example:
        container = Container()
        container.register(Clock, lambda: SystemClock(), lifetime=Lifetime.SINGLETON)
        clock = container.resolve(Clock)

    Constructor auto-wiring: if a registered factory is a plain class,
    the container inspects its ``__init__`` type hints and resolves each
    parameter from the container itself, recursively.
    """

    def __init__(self, parent: Container | None = None) -> None:
        self._registrations: dict[type, _Registration] = {}
        self._scoped_instances: dict[type, Any] = {}
        self._resolving: list[type] = []
        self._parent = parent
        self._in_scope = False

    # -- registration ----------------------------------------------------

    def register(
        self,
        key: type[T],
        factory: Factory | None = None,
        *,
        lifetime: Lifetime = Lifetime.SINGLETON,
    ) -> Self:
        """Register a factory (or the class itself) for `key`.

        If `factory` is omitted, `key` is used as its own factory, and its
        constructor arguments are auto-resolved from the container.
        """
        resolved_factory: Factory = factory if factory is not None else key
        self._registrations[key] = _Registration(factory=resolved_factory, lifetime=lifetime)
        return self

    def register_instance(self, key: type[T], instance: T) -> Self:
        """Register an already-constructed instance as a singleton."""
        self._registrations[key] = _Registration(
            factory=lambda: instance, lifetime=Lifetime.SINGLETON, instance=instance
        )
        return self

    def is_registered(self, key: type) -> bool:
        if key in self._registrations:
            return True
        if self._parent is not None:
            return self._parent.is_registered(key)
        return False

    # -- resolution --------------------------------------------------------

    def resolve(self, key: type[T]) -> T:
        """Resolve an instance of `key`, constructing dependencies as needed."""
        if key in self._resolving:
            raise CircularDependencyError(self._resolving + [key])

        registration = self._find_registration(key)
        if registration is None:
            raise UnregisteredDependencyError(key)

        if registration.lifetime == Lifetime.SINGLETON and registration.instance is not None:
            return registration.instance

        if registration.lifetime == Lifetime.SCOPED and self._in_scope and key in self._scoped_instances:
            return self._scoped_instances[key]

        self._resolving.append(key)
        try:
            instance = self._instantiate(registration.factory)
        finally:
            self._resolving.pop()

        if registration.lifetime == Lifetime.SINGLETON:
            registration.instance = instance
        elif registration.lifetime == Lifetime.SCOPED and self._in_scope:
            self._scoped_instances[key] = instance

        return instance

    def _find_registration(self, key: type) -> _Registration | None:
        if key in self._registrations:
            return self._registrations[key]
        if self._parent is not None:
            return self._parent._find_registration(key)
        return None

    def _instantiate(self, factory: Factory) -> Any:
        """Call `factory`, auto-resolving any parameters it declares."""
        if not (inspect.isclass(factory) or inspect.isfunction(factory) or inspect.ismethod(factory)):
            # e.g. a lambda or already-bound callable with no introspectable
            # signature worth walking — just call it directly.
            return factory()

        try:
            hints = get_type_hints(factory.__init__ if inspect.isclass(factory) else factory)
        except (TypeError, NameError):
            hints = {}

        sig = inspect.signature(factory)
        kwargs: dict[str, Any] = {}
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            annotation = hints.get(name, param.annotation)
            if annotation is inspect.Parameter.empty:
                if param.default is inspect.Parameter.empty:
                    raise ContainerError(
                        f"Cannot auto-wire {factory!r}: parameter '{name}' has no "
                        f"type hint and no default value."
                    )
                continue
            if self.is_registered(annotation):
                kwargs[name] = self.resolve(annotation)
            elif param.default is inspect.Parameter.empty:
                raise UnregisteredDependencyError(annotation)

        return factory(**kwargs)

    # -- scoping -----------------------------------------------------------

    @contextmanager
    def scope(self) -> Iterator[Container]:
        """Open a resolution scope for SCOPED-lifetime registrations.

        Example:
            with container.scope() as scoped:
                a = scoped.resolve(RequestContext)
                b = scoped.resolve(RequestContext)  # same instance as `a`
            # scope ends: scoped instances are discarded
        """
        child = Container(parent=self)
        child._in_scope = True
        try:
            yield child
        finally:
            child._scoped_instances.clear()
