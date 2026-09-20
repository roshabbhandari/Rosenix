from rosenix.defaults import with_defaults


def test_with_defaults_preserves_explicit_values():
    assert with_defaults({"timeout": 5}, {"timeout": 30, "retries": 2}) == {"timeout": 5, "retries": 2}
