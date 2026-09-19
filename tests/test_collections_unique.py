from rosenix.collections import unique


def test_unique_preserves_first_occurrence_order():
    assert unique([3, 1, 3, 2, 1]) == [3, 1, 2]
