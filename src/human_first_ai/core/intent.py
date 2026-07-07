"""Structured representation of what a human is asking the system to do."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ActionClass(Enum):
    """How consequential is this action, in terms of human agency?"""

    INFORMATIONAL = "informational"    # answering, reading, no side effects
    REVERSIBLE = "reversible"          # can be undone (e.g. saving a draft)
    IRREVERSIBLE = "irreversible"      # cannot be undone (e.g. sending an email, spending money)


@dataclass
class Intent:
    """A structured request produced by the Perception step."""

    description: str
    action_class: ActionClass
    requires_memory: bool = False
    requires_new_consent: bool = False
    payload: dict[str, Any] = field(default_factory=dict)
    source: Optional[str] = None
