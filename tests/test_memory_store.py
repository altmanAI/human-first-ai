import pytest

from human_first_ai.memory.store import MemoryItem, MemoryStore


def test_remember_and_recall():
    store = MemoryStore()
    store.remember(MemoryItem(content="likes oat milk lattes", origin="user said so", consented=True))
    results = store.recall("oat milk")
    assert len(results) == 1


def test_forget_removes_matching_items():
    store = MemoryStore()
    store.remember(MemoryItem(content="likes oat milk lattes", origin="user said so", consented=True))
    removed = store.forget("oat milk")
    assert removed == 1
    assert store.recall("oat milk") == []


def test_long_term_without_consent_raises():
    store = MemoryStore()
    with pytest.raises(PermissionError):
        store.remember(MemoryItem(content="some fact", origin="inferred", consented=False, long_term=True))


def test_long_term_with_consent_is_listed():
    store = MemoryStore()
    store.remember(MemoryItem(content="prefers morning meetings", origin="user said so", consented=True, long_term=True))
    assert len(store.all_long_term()) == 1
