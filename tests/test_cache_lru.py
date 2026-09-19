import pytest

from rosenix.cache import LRUCache


def test_lru_cache_evicts_least_recently_used_item():
    cache = LRUCache(capacity=2)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.get("a") == 1
    cache.set("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_lru_cache_rejects_non_positive_capacity():
    with pytest.raises(ValueError):
        LRUCache(capacity=0)
