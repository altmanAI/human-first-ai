# Architecture

Human-First AI is organized as a pipeline of four modules plus a cross-cutting transparency layer. Each module is deliberately small and single-purpose so it can be read, audited, and replaced independently.

## 1. Perception (`src/human_first_ai/core`)

Takes raw input (a message, an event, a trigger) and produces a structured `Intent` — what the human is asking for, what context is relevant, and what kind of action class this might require (informational, reversible, irreversible/external).

## 2. Values Engine (`src/human_first_ai/values`)

Every `Intent` passes through the Values Engine before anything else happens. It evaluates the intent against a small, explicit policy set:

- **Consent check** — does fulfilling this require memory or data the human hasn't approved?
- **Reversibility check** — is this action reversible, or does it need a human checkpoint?
- **Boundary check** — does this action fall inside the human's configured boundaries (e.g. "never post publicly without approval")?

The engine returns an `Allow`, `AllowWithCheckpoint`, or `Deny` decision plus a plain-language reason — the same reason that will later show up in the transparency log.

## 3. Memory Layer (`src/human_first_ai/memory`)

A minimal, inspectable memory store. Key properties:

- Every stored item has an origin (why it was remembered) and a consent flag.
- Memory is queryable and deletable by the human at any time — `forget(query)` is a first-class operation, not an afterthought.
- Short-term (session) and long-term (persisted) memory are explicitly separated so nothing "graduates" to permanent storage silently.

## 4. Action Layer (`src/human_first_ai/core`)

Executes the intent once the Values Engine has approved it. If the decision was `AllowWithCheckpoint`, the Action Layer pauses and surfaces a plain-language confirmation to the human before proceeding.

## 5. Transparency Log (`src/human_first_ai/transparency`)

Every decision — allowed, checkpointed, or denied — is written to an append-only, human-readable log. The log format is intentionally a plain sentence, not a JSON blob dump: *"Remembered that you prefer morning meetings, because you told me directly on 2026-07-02."*

## Data flow

```
Intent → Values Engine → (Deny → stop, log, explain)
                        → (AllowWithCheckpoint → ask human → proceed or stop)
                        → (Allow → Memory Layer → Action Layer)
                                                        ↓
                                              Transparency Log (always)
```

## Extending this

- Swap in your own LLM/reasoning engine at the Perception step — the rest of the pipeline is model-agnostic.
- Add new policies to the Values Engine as plain functions — no framework lock-in.
- Back the Memory Layer with any store (SQLite, Postgres, vector DB) by implementing the `MemoryStore` interface.
