import pytest

from rosenix.kernel.container import (
    CircularDependencyError,
    Container,
    Lifetime,
    UnregisteredDependencyError,
)


class Clock:
    def now(self) -> int:
        return 42


class Service:
    def __init__(self, clock: Clock) -> None:
        self.clock = clock


class _CircularA:
    def __init__(self, b: "_CircularB") -> None:
        self.b = b


class _CircularB:
    def __init__(self, a: _CircularA) -> None:
        self.a = a


def test_resolve_singleton_returns_same_instance():
    container = Container()
    container.register(Clock)
    a = container.resolve(Clock)
    b = container.resolve(Clock)
    assert a is b


def test_resolve_transient_returns_new_instance():
    container = Container()
    container.register(Clock, lifetime=Lifetime.TRANSIENT)
    a = container.resolve(Clock)
    b = container.resolve(Clock)
    assert a is not b


def test_auto_wires_constructor_dependencies():
    container = Container()
    container.register(Clock)
    container.register(Service)
    service = container.resolve(Service)
    assert isinstance(service.clock, Clock)


def test_unregistered_dependency_raises():
    container = Container()
    with pytest.raises(UnregisteredDependencyError):
        container.resolve(Clock)


def test_register_instance_returns_exact_object():
    container = Container()
    clock = Clock()
    container.register_instance(Clock, clock)
    assert container.resolve(Clock) is clock


def test_scope_shares_instance_within_scope_only():
    class Scoped:
        pass

    container = Container()
    container.register(Scoped, lifetime=Lifetime.SCOPED)

    with container.scope() as scope_a:
        a1 = scope_a.resolve(Scoped)
        a2 = scope_a.resolve(Scoped)
        assert a1 is a2

    with container.scope() as scope_b:
        b1 = scope_b.resolve(Scoped)
        assert b1 is not a1


def test_circular_dependency_detected():
    # Defined at module scope (not nested) so `get_type_hints` can resolve
    # the forward reference to `_CircularB` without a NameError.
    container = Container()
    container.register(_CircularA)
    container.register(_CircularB)

    with pytest.raises(CircularDependencyError):
        container.resolve(_CircularA)
