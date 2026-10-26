"""Print the agent and judge prompt templates verbatim as Markdown (for the paper's appendix).
Run from lab/:  uv run python ../projects/2026-10-apart-collusion-sprint/report/export_prompts.py
"""
from epistemic_lab import prompts

parts = [
    ("Objective text inserted into each agent's prompt (one of three)", "\n".join(f"{k}: {v}" for k, v in prompts.OBJECTIVE.items())),
    ("Note appended to the proposer's objective in regime E1q only", prompts.REVIEWER_RULE_NOTE.strip()),
    ("Proposer", prompts.PROPOSER), ("Reviewer", prompts.REVIEWER), ("Reviewer, private reply", prompts.REVIEWER_REPLY),
    ("Decider", prompts.DECIDER), ("LLM judge", prompts.JUDGE),
]
for title, text in parts:
    print(f"**{title}.**\n\n```\n{text.strip()}\n```\n")
