# Vision

## The problem

AI systems today are mostly built backwards. Teams start with "what can this model do?" and bolt on safety, consent, and transparency at the end — as a compliance checkbox rather than an architectural principle. The result: systems that surprise users, remember things they never agreed to, take actions they can't explain, and treat "alignment" as a system prompt instead of an enforced code path.

## The premise

If an AI system is going to sit close to someone's life — their messages, their calendar, their money, their decisions — the design has to earn that closeness. That means:

- The human should never be surprised by what the system remembers.
- The human should never be surprised by what the system did on their behalf.
- The human should always be able to ask "why did you do that?" and get a real answer, not a shrug.
- The human should always be able to say "stop remembering that" and have it actually stop.

None of this is a feature bolted onto a chatbot. It's a set of load-bearing components: a **Values Engine** that every action routes through, a **Memory Layer** that treats consent as a first-class field, and a **Transparency Log** that turns every decision into something a non-technical person can read and understand.

## Design principles

1. **Reversibility first.** Prefer actions that can be undone. When an action can't be undone (sending an email, spending money, posting publicly), require an explicit human checkpoint.
2. **Boring is good.** The Values Engine should be simple enough to read start to finish in five minutes. Alignment logic hidden in thousands of lines of orchestration code is alignment theater.
3. **Memory is a privilege, not a default.** Systems should start with the least memory necessary and expand only with explicit, inspectable consent.
4. **Explainability is a UX requirement, not a research goal.** If the audit log needs a PhD to parse, it isn't transparency — it's paperwork.
5. **The human is the client, not the training signal.** Optimize for the person's stated goals and wellbeing, not for engagement, retention, or any other proxy metric.

## What this is not

- Not a new foundation model. This framework is model-agnostic — plug in whatever LLM or reasoning engine you want.
- Not a full safety/alignment research project. It's a practical, adoptable pattern for people building assistant-style AI systems today.
- Not finished. This is a seed. The most valuable contributions will be the ones that push these principles further, not just add features.
