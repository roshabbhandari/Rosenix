import pytest

from rosenix.kernel.registry import Registry


def test_register_and_get_returns_loaded_object():
    registry = Registry()
    registry.register("my-provider", lambda: {"name": "my-provider"})
    assert registry.get("my-provider") == {"name": "my-provider"}


def test_get_is_lazy_until_called():
    calls = []

    def loader():
        calls.append(1)
        return object()

    registry = Registry()
    registry.register("lazy", loader)
    assert calls == []  # not loaded yet
    registry.get("lazy")
    assert calls == [1]


def test_get_unknown_plugin_raises_with_available_names():
    registry = Registry()
    registry.register("known", lambda: object())
    with pytest.raises(KeyError, match="known"):
        registry.get("missing")


def test_names_lists_registered_plugins():
    registry = Registry()
    registry.register("a", lambda: object())
    registry.register("b", lambda: object())
    assert registry.names() == ["a", "b"]


def test_separate_groups_do_not_collide():
    registry = Registry()
    registry.register("shared-name", lambda: "in-group-1", group="group1")
    registry.register("shared-name", lambda: "in-group-2", group="group2")
    assert registry.get("shared-name", group="group1") == "in-group-1"
    assert registry.get("shared-name", group="group2") == "in-group-2"
