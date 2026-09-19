from rosenix.collections import first


def test_first_returns_default_for_empty_iterable():
    assert first([], default="fallback") == "fallback"


def test_first_returns_first_item_from_generator():
    assert first(value for value in [7, 8, 9]) == 7
