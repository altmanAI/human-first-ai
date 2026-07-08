# Human-First AI

**The reference architecture for AltmanAI's P.A.I.H.I. framework — a small, readable, working implementation of what "human-first AI" actually means in code, not just in a pitch deck.**

Built by [AltmanAI](https://github.com/altmanAI), a project of Altman Family Group LLC.

---

## Why this exists

Most AI systems are optimized for capability first and humanity second — if at all. Human-First AI flips that: every architectural decision starts from the question *"does this respect the person on the other end?"* before *"is this impressive?"*

This repo is both a **philosophy** and a **working reference implementation** — a small, readable core you can fork, learn from, or build production systems on top of. It's also the place where AltmanAI's **P.A.I.H.I. framework** stops being a slide and becomes code that actually runs and scores a session.

## P.A.I.H.I. — the framework this implements

| | Dimension | What it means here |
|---|---|---|
| **P** | **Proof** | Every decision is grounded in a real, inspectable log — not a black box. |
| **A** | **Alignment** | Every action passes through an explicit Values Engine before anything happens — alignment is a first-class module, not a prompt suffix. |
| **I** | **Integrity** | Memory is consent-based and boundaried. Nothing is persisted long-term without explicit, inspectable consent. |
| **H** | **Humanity** | Irreversible or external actions require a human checkpoint. The human always has a steering wheel, and the system honors whatever they decide. |
| **I** | **Impact** | Did the system actually complete something real — not just talk, decline, or stall? |

`human_first_ai.paihi.PAIHIScorer` computes a live 0–100 score across all five dimensions from an actual run of the pipeline — see [Quickstart](#quickstart) below.

## Architecture

```
                 ┌────────────────────┐
   Input   ───▶  │   Perception       │
                 │   (context, intent) │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │   Values Engine    │◀── consent + policy config      [Alignment]
                 │  (guardrail checks) │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │   Memory Layer     │◀── inspectable, forgettable     [Integrity]
                 │ (short/long term)   │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │   Action Layer     │──▶ human checkpoint (if needed) [Humanity]
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │  Transparency Log  │──▶ human-readable audit trail   [Proof]
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │   PAIHI Scorer     │──▶ 0-100 score, 5 dimensions    [Impact + all]
                 └────────────────────┘
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full breakdown and [`docs/VISION.md`](docs/VISION.md) for the reasoning behind each design choice.

## Quickstart

```bash
git clone https://github.com/altmanAI/human-first-ai.git
cd human-first-ai
pip install -e ".[dev]"
python -m human_first_ai.demo
```

The demo processes three intents (informational, irreversible-with-checkpoint, boundary-violating) and ends by printing a real **P.A.I.H.I. Score** for that session:

```
--- P.A.I.H.I. Score for this session ---
P — Proof:      100.0/100  (grounded in a real, inspectable log)
A — Alignment:  100.0/100  (every action passed the Values Engine)
I — Integrity:  100.0/100  (no memory persisted without consent)
H — Humanity:   100.0/100  (checkpoints honored, human stayed in control)
I — Impact:      66.7/100  (real actions completed, not just talk)
----------------------------------------------------
Overall P.A.I.H.I. Score: 93.3/100
```

## Project layout

```
src/human_first_ai/
  core/           orchestrator that wires perception → values → memory → action
  values/         the alignment / guardrail engine
  memory/         consent-based, inspectable memory store
  transparency/   audit logging and plain-language explanations
  paihi/          the P.A.I.H.I. Scorer — turns the framework into a number
docs/             architecture + vision docs
tests/            unit tests for each module (20 tests, all passing)
```

## Status

Early, intentionally minimal reference implementation. The goal isn't feature completeness — it's a clean pattern others can adopt, extend, challenge, or score their own systems against.

## Contributing

Issues and PRs welcome — especially ones that make the system *more* transparent or *more* respectful of human agency, not just more capable. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and our [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## License

MIT © Altman Family Group LLC — see [`LICENSE`](LICENSE).
