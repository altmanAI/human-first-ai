from human_first_ai.core import Intent, ActionClass, Orchestrator
from human_first_ai.values import ValuesEngine
from human_first_ai.memory import MemoryStore, MemoryItem
from human_first_ai.paihi import PAIHIScorer, PAIHIScore, RunRecord
from human_first_ai.values.engine import Decision, DecisionType


def test_clean_run_scores_perfectly_across_all_dimensions():
    values = ValuesEngine()
    orch = Orchestrator(values_engine=values)
    orch.process(Intent("summarize today's calendar", ActionClass.INFORMATIONAL))

    score = PAIHIScorer().score(orch.runs, log=orch.log, memory=orch.memory)
    assert isinstance(score, PAIHIScore)
    assert score.proof == 100.0
    assert score.alignment == 100.0
    assert score.integrity == 100.0
    assert score.humanity == 100.0
    assert score.impact == 100.0
    assert score.overall == 100.0


def test_boundary_violation_drags_down_impact_not_alignment():
    values = ValuesEngine(boundaries=["post publicly"])
    orch = Orchestrator(values_engine=values)
    orch.process(Intent("post publicly about launch", ActionClass.IRREVERSIBLE))

    score = PAIHIScorer().score(orch.runs, log=orch.log, memory=orch.memory)
    # Denied action: still logged (proof) and still had a real reason (alignment),
    # but impact drops because nothing was actually completed.
    assert score.proof == 100.0
    assert score.alignment == 100.0
    assert score.impact == 0.0


def test_declined_checkpoint_lowers_humanity_only_if_not_honored():
    values = ValuesEngine()
    orch = Orchestrator(values_engine=values, checkpoint_fn=lambda intent, reason: False)
    orch.process(Intent("send an email", ActionClass.IRREVERSIBLE))

    score = PAIHIScorer().score(orch.runs, log=orch.log, memory=orch.memory)
    # The human said no, and the system stopped -- that IS the checkpoint being
    # honored, so humanity should be 100, even though impact is 0.
    assert score.humanity == 100.0
    assert score.impact == 0.0


def test_unconsented_long_term_memory_zeroes_integrity():
    memory = MemoryStore()
    # Bypass the store's own guard to simulate a corrupted/legacy record.
    memory._long_term.append(
        MemoryItem(content="secret", origin="inferred", consented=False, long_term=True)
    )
    runs = [
        RunRecord(
            decision=Decision(decision=DecisionType.ALLOW, reason="ok"),
        )
    ]
    from human_first_ai.transparency import TransparencyLog

    log = TransparencyLog()
    log.record("ok")

    score = PAIHIScorer().score(runs, log=log, memory=memory)
    assert score.integrity == 0.0


def test_render_includes_all_five_letters():
    score = PAIHIScore(proof=90, alignment=80, integrity=100, humanity=70, impact=60)
    text = score.render()
    for letter in ["Proof", "Alignment", "Integrity", "Humanity", "Impact", "Overall"]:
        assert letter in text
