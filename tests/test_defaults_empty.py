from rosenix.defaults import with_defaults


def test_with_defaults_returns_copy_for_empty_values():
    defaults = {"mode": "safe"}
    assert with_defaults({}, defaults) == defaults
