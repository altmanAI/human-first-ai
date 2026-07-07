from human_first_ai.core import Intent, ActionClass, Orchestrator
from human_first_ai.values import ValuesEngine, DecisionType


def test_informational_intent_is_allowed():
    values = ValuesEngine()
    intent = Intent(description="what's on my calendar today", action_class=ActionClass.INFORMATIONAL)
    decision = values.evaluate(intent)
    assert decision.decision == DecisionType.ALLOW


def test_irreversible_intent_requires_checkpoint():
    values = ValuesEngine()
    intent = Intent(description="send an email to the team", action_class=ActionClass.IRREVERSIBLE)
    decision = values.evaluate(intent)
    assert decision.decision == DecisionType.ALLOW_WITH_CHECKPOINT


def test_boundary_violation_is_denied():
    values = ValuesEngine(boundaries=["post publicly"])
    intent = Intent(description="post publicly about the launch", action_class=ActionClass.IRREVERSIBLE)
    decision = values.evaluate(intent)
    assert decision.decision == DecisionType.DENY


def test_orchestrator_denies_boundary_violation():
    values = ValuesEngine(boundaries=["post publicly"])
    orch = Orchestrator(values_engine=values)
    intent = Intent(description="post publicly about the launch", action_class=ActionClass.IRREVERSIBLE)
    result = orch.process(intent)
    assert result.startswith("Declined")


def test_orchestrator_checkpoint_can_be_declined():
    values = ValuesEngine()
    orch = Orchestrator(values_engine=values, checkpoint_fn=lambda intent, reason: False)
    intent = Intent(description="send an email", action_class=ActionClass.IRREVERSIBLE)
    result = orch.process(intent)
    assert result.startswith("Stopped")


def test_memory_forget_removes_items():
    from human_first_ai.memory import MemoryStore, MemoryItem

    store = MemoryStore()
    store.remember(MemoryItem(content="likes morning meetings", origin="user told me directly"))
    assert len(store.recall("morning meetings")) == 1
    removed = store.forget("morning meetings")
    assert removed == 1
    assert len(store.recall("morning meetings")) == 0


def test_memory_refuses_long_term_without_consent():
    from human_first_ai.memory import MemoryStore, MemoryItem
    import pytest

    store = MemoryStore()
    with pytest.raises(PermissionError):
        store.remember(
            MemoryItem(content="secret", origin="inferred", consented=False, long_term=True)
        )
