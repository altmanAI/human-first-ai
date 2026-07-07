"""An append-only, human-readable audit log.

Every entry is a plain sentence a non-technical person could read and
understand — not a JSON blob dump. Explainability is a UX requirement here,
not a research goal.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LogEntry:
    timestamp: datetime
    summary: str  # e.g. "Remembered that you prefer morning meetings, because you told me directly."


class TransparencyLog:
    def __init__(self):
        self._entries: list[LogEntry] = []

    def record(self, summary: str) -> LogEntry:
        entry = LogEntry(timestamp=datetime.now(timezone.utc), summary=summary)
        self._entries.append(entry)
        return entry

    def history(self) -> list[LogEntry]:
        return list(self._entries)

    def render(self) -> str:
        """Human-readable transcript of everything the system has done and why."""
        lines = []
        for e in self._entries:
            ts = e.timestamp.strftime("%Y-%m-%d %H:%M UTC")
            lines.append(f"[{ts}] {e.summary}")
        return "\n".join(lines)
