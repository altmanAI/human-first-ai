"""The Values Engine — every Intent passes through here before anything happens.

Deliberately small and readable: alignment logic you can read start to finish
in a few minutes, not buried in thousands of lines of orchestration code.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from ..core.intent import ActionClass, Intent


class DecisionType(Enum):
    ALLOW = "allow"
    ALLOW_WITH_CHECKPOINT = "allow_with_checkpoint"
    DENY = "deny"


@dataclass
class Decision:
    decision: DecisionType
    reason: str  # plain-language, human-readable — this is what ends up in the log


PolicyFn = Callable[[Intent], Optional[Decision]]


class ValuesEngine:
    """Evaluates an Intent against a small, explicit set of policies.

    Policies run in order; the first one that returns a Decision wins.
    If no policy fires, the default is Allow.
    """

    def __init__(self, boundaries: Optional[list[str]] = None):
        # Boundaries are plain strings describing things the human has said
        # should never happen automatically, e.g. "never post publicly".
        self.boundaries = boundaries or []
        self._policies: list[PolicyFn] = [
            self._consent_check,
            self._boundary_check,
            self._reversibility_check,
        ]

    def evaluate(self, intent: Intent) -> Decision:
        for policy in self._policies:
            result = policy(intent)
            if result is not None:
                return result
        return Decision(
            decision=DecisionType.ALLOW,
            reason=f"'{intent.description}' is informational and reversible — proceeding.",
        )

    # -- built-in policies -------------------------------------------------

    def _consent_check(self, intent: Intent) -> Optional[Decision]:
        if intent.requires_new_consent:
            return Decision(
                decision=DecisionType.ALLOW_WITH_CHECKPOINT,
                reason=(
                    f"'{intent.description}' would require remembering or accessing "
                    "something new — checking with you first."
                ),
            )
        return None

    def _boundary_check(self, intent: Intent) -> Optional[Decision]:
        for boundary in self.boundaries:
            if boundary.lower() in intent.description.lower():
                return Decision(
                    decision=DecisionType.DENY,
                    reason=f"'{intent.description}' conflicts with your boundary: \"{boundary}\".",
                )
        return None

    def _reversibility_check(self, intent: Intent) -> Optional[Decision]:
        if intent.action_class == ActionClass.IRREVERSIBLE:
            return Decision(
                decision=DecisionType.ALLOW_WITH_CHECKPOINT,
                reason=(
                    f"'{intent.description}' can't be undone once it happens — "
                    "confirming with you before proceeding."
                ),
            )
        return None
