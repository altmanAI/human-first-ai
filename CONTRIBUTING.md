# Contributing

Thanks for considering a contribution to Human-First AI.

## Ground rule

Every PR should be evaluated against one question: **does this make the system more respectful of human agency, or just more capable?** Capability without respect isn't a contribution here — plenty of other projects optimize for that. This one optimizes for trust.

## Getting started

```bash
git clone https://github.com/altmanAI/human-first-ai.git
cd human-first-ai
pip install -e ".[dev]"
pytest -q
```

## What we're looking for

- New policies for the Values Engine (as small, readable functions).
- Additional `MemoryStore` backends (SQLite, Postgres, vector DBs) implementing the same interface.
- Clearer, more human-readable transparency log formats.
- Real-world integrations that demonstrate the pattern (a Slack bot, a scheduling assistant, etc.) — as examples, not as scope creep into the core.

## What we're not looking for

- Features that quietly expand what the system remembers or does without a corresponding consent/transparency path.
- Complexity for its own sake. If a change can't be explained in a sentence, it needs to be simplified before it's merged.

## Pull requests

1. Fork and branch from `main`.
2. Add or update tests for any behavior change.
3. Keep PRs focused — one idea per PR.
4. Describe *why* in the PR description, not just *what*.
