"""A minimal, inspectable, consent-based memory store.

Design goals:
- Every item knows *why* it was remembered (origin) and whether it was consented to.
- Short-term and long-term memory are explicitly separate — nothing "graduates"
  to permanent storage silently.
- Forgetting is a first-class operation, not an afterthought.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class MemoryItem:
    content: str
    origin: str            # why this was remembered, in plain language
    consented: bool = False
    long_term: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryStore:
    """In-memory reference implementation. Swap for SQLite/Postgres/vector DB
    in production by implementing the same interface."""

    def __init__(self):
        self._short_term: list[MemoryItem] = []
        self._long_term: list[MemoryItem] = []

    def remember(self, item: MemoryItem) -> MemoryItem:
        if item.long_term and not item.consented:
            raise PermissionError(
                f"Refusing to persist '{item.content}' to long-term memory without consent."
            )
        (self._long_term if item.long_term else self._short_term).append(item)
        return item

    def recall(self, query: str) -> list[MemoryItem]:
        pool = self._short_term + self._long_term
        return [m for m in pool if query.lower() in m.content.lower()]

    def forget(self, query: str) -> int:
        """Remove any memory matching the query. Returns count removed."""
        before = len(self._short_term) + len(self._long_term)
        self._short_term = [m for m in self._short_term if query.lower() not in m.content.lower()]
        self._long_term = [m for m in self._long_term if query.lower() not in m.content.lower()]
        after = len(self._short_term) + len(self._long_term)
        return before - after

    def all_long_term(self) -> list[MemoryItem]:
        """Everything persisted — a human should always be able to see this list."""
        return list(self._long_term)
