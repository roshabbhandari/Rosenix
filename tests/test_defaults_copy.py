from rosenix.defaults import with_defaults


def test_with_defaults_does_not_mutate_defaults_mapping():
    defaults = {"retries": 2}
    result = with_defaults({}, defaults)
    result["retries"] = 5
    assert defaults == {"retries": 2}
