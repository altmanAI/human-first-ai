from human_first_ai.core.intent import ActionClass, Intent
from human_first_ai.values.engine import DecisionType, ValuesEngine


def test_informational_intent_is_allowed():
    engine = ValuesEngine()
    intent = Intent("Answer a question", ActionClass.INFORMATIONAL)
    decision = engine.evaluate(intent)
    assert decision.decision == DecisionType.ALLOW


def test_irreversible_intent_requires_checkpoint():
    engine = ValuesEngine()
    intent = Intent("Send an email", ActionClass.IRREVERSIBLE)
    decision = engine.evaluate(intent)
    assert decision.decision == DecisionType.ALLOW_WITH_CHECKPOINT


def test_new_consent_requirement_triggers_checkpoint():
    engine = ValuesEngine()
    intent = Intent(
        "Remember a new fact",
        ActionClass.REVERSIBLE,
        requires_memory=True,
        requires_new_consent=True,
    )
    decision = engine.evaluate(intent)
    assert decision.decision == DecisionType.ALLOW_WITH_CHECKPOINT


def test_boundary_violation_is_denied():
    engine = ValuesEngine(boundaries=["post publicly"])
    intent = Intent("Post publicly to social media", ActionClass.IRREVERSIBLE)
    decision = engine.evaluate(intent)
    assert decision.decision == DecisionType.DENY
