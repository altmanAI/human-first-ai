"""Wires Perception -> Values Engine -> Memory -> Action -> Transparency Log
into a single pipeline. This is the load-bearing piece of Human-First AI."""

from typing import Callable, Optional

from .intent import Intent
from ..values.engine import ValuesEngine, DecisionType
from ..memory.store import MemoryStore, MemoryItem
from ..transparency.log import TransparencyLog

# A checkpoint function takes the intent + reason and returns True (proceed)
# or False (human declined). Default: auto-approve, for demo purposes only —
# real deployments should wire this to an actual human confirmation prompt.
CheckpointFn = Callable[[Intent, str], bool]


def _default_checkpoint(intent: Intent, reason: str) -> bool:
    print(f"[checkpoint] {reason}\n  -> auto-approving (wire up a real prompt in production)")
    return True


class Orchestrator:
    def __init__(
        self,
        values_engine: Optional[ValuesEngine] = None,
        memory: Optional[MemoryStore] = None,
        log: Optional[TransparencyLog] = None,
        checkpoint_fn: CheckpointFn = _default_checkpoint,
        action_fn: Optional[Callable[[Intent], str]] = None,
    ):
        self.values = values_engine or ValuesEngine()
        self.memory = memory or MemoryStore()
        self.log = log or TransparencyLog()
        self.checkpoint_fn = checkpoint_fn
        self.action_fn = action_fn or (lambda intent: f"Executed: {intent.description}")

    def process(self, intent: Intent) -> str:
        decision = self.values.evaluate(intent)
        self.log.record(decision.reason)

        if decision.decision == DecisionType.DENY:
            return f"Declined — {decision.reason}"

        if decision.decision == DecisionType.ALLOW_WITH_CHECKPOINT:
            approved = self.checkpoint_fn(intent, decision.reason)
            if not approved:
                self.log.record(f"You declined: '{intent.description}'. No action taken.")
                return "Stopped — you declined the checkpoint."

        if intent.requires_memory:
            item = self.memory.remember(
                MemoryItem(
                    content=intent.description,
                    origin=decision.reason,
                    consented=not intent.requires_new_consent or decision.decision != DecisionType.DENY,
                    long_term=False,
                )
            )
            self.log.record(f"Stored in short-term memory: '{item.content}'.")

        result = self.action_fn(intent)
        self.log.record(f"Completed: '{intent.description}'.")
        return result
