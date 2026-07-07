"""Run with: python -m human_first_ai.demo

A tiny walkthrough of the pipeline: one informational request, one that
requires a checkpoint, and one that violates a stated boundary.
"""

from human_first_ai.core import Intent, ActionClass, Orchestrator
from human_first_ai.values import ValuesEngine


def main():
    values = ValuesEngine(boundaries=["post publicly"])
    orch = Orchestrator(values_engine=values)

    examples = [
        Intent(
            description="summarize today's calendar",
            action_class=ActionClass.INFORMATIONAL,
        ),
        Intent(
            description="send an email to the client confirming the meeting",
            action_class=ActionClass.IRREVERSIBLE,
        ),
        Intent(
            description="post publicly about the new product launch",
            action_class=ActionClass.IRREVERSIBLE,
        ),
    ]

    for intent in examples:
        print(f"\n> {intent.description}")
        print(orch.process(intent))

    print("\n--- Transparency Log ---")
    print(orch.log.render())


if __name__ == "__main__":
    main()
