"""Wires Perception -> Values Engine -> Memory -> Action -> Transparency Log
into a single pipeline. This is the load-bearing piece of Human-First AI."""

from typing import Callable, Optional

from .intent import Intent
from ..values.engine import ValuesEngine, DecisionType
from ..memory.store import MemoryStore, MemoryItem
from ..transparency.log import TransparencyLog
from ..paihi.score import RunRecord

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
        # Every processed Intent appends a RunRecord here — feed this list
        # straight into PAIHIScorer.score() to get a P.A.I.H.I. Score for
        # this session. See human_first_ai.paihi.
        self.runs: list[RunRecord] = []

    def process(self, intent: Intent) -> str:
        decision = self.values.evaluate(intent)
        self.log.record(decision.reason)

        checkpoint_offered = decision.decision == DecisionType.ALLOW_WITH_CHECKPOINT

        if decision.decision == DecisionType.DENY:
            self.runs.append(RunRecord(decision=decision, checkpoint_offered=False))
            return f"Declined — {decision.reason}"

        if checkpoint_offered:
            approved = self.checkpoint_fn(intent, decision.reason)
            # "Honored" means the system did what the human's checkpoint answer
            # said -- whether that answer was yes or no. The orchestrator always
            # respects it structurally; this flag exists so a scorer (or a bugged
            # future implementation that ignores the answer) has something real
            # to check, instead of assuming honesty.
            if not approved:
                self.log.record(f"You declined: '{intent.description}'. No action taken.")
                self.runs.append(
                    RunRecord(
                        decision=decision,
                        checkpoint_offered=True,
                        checkpoint_honored=True,
                        completed=False,
                    )
                )
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
        self.runs.append(
            RunRecord(
                decision=decision,
                checkpoint_offered=checkpoint_offered,
                checkpoint_honored=True if checkpoint_offered else None,
                completed=True,
            )
        )
        return result
