# Human-First AI

**A reference architecture and framework for building AI systems that put people — not just performance — at the center.**

Built by [AltmanAI](https://github.com/altmanAI), a project of Altman Family Group LLC.

---

## Why this exists

Most AI systems are optimized for capability first and humanity second — if at all. Human-First AI flips that: every architectural decision starts from the question *"does this respect the person on the other end?"* before *"is this impressive?"*

This repo is both a **philosophy** and a **working reference implementation** — a small, readable core you can fork, learn from, or build production systems on top of.

## The five commitments

1. **Consent over assumption** — the system never silently expands what it remembers or does without the human knowing.
2. **Transparency over magic** — every consequential action is logged and explainable in plain language, not hidden behind a black box.
3. **Human-in-the-loop by default** — irreversible or external actions require a checkpoint; the human always has a steering wheel.
4. **Memory with boundaries** — long-term memory is opt-in, inspectable, and forgettable. Nothing is permanent unless the human wants it to be.
5. **Values as code, not vibes** — alignment isn't a prompt suffix. It's a first-class module that every action passes through.

## Architecture

```
                 ┌────────────────────┐
   Input   ───▶  │   Perception       │
                 │   (context, intent) │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │   Values Engine    │◀── consent + policy config
                 │  (guardrail checks) │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │   Memory Layer     │◀── inspectable, forgettable
                 │ (short/long term)   │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │   Action Layer     │──▶ human checkpoint (if needed)
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │  Transparency Log  │──▶ human-readable audit trail
                 └────────────────────┘
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full breakdown and [`docs/VISION.md`](docs/VISION.md) for the reasoning behind each design choice.

## Quickstart

```bash
git clone https://github.com/altmanAI/human-first-ai.git
cd human-first-ai
pip install -e .
python -m human_first_ai.demo
```

## Project layout

```
src/human_first_ai/
  core/           orchestrator that wires perception → values → memory → action
  values/         the alignment / guardrail engine
  memory/         consent-based, inspectable memory store
  transparency/   audit logging and plain-language explanations
docs/             architecture + vision docs
tests/            unit tests for each module
```

## Status

Early, intentionally minimal reference implementation. The goal isn't feature completeness — it's a clean pattern others can adopt, extend, or challenge.

## Contributing

Issues and PRs welcome — especially ones that make the system *more* transparent or *more* respectful of human agency, not just more capable. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and our [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## License

MIT © Altman Family Group LLC — see [`LICENSE`](LICENSE).
