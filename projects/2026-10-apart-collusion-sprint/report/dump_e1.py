"""Print the private messages, votes, and decision of every E1 trajectory of a run, for hand reading.
Run from lab/:  uv run python ../projects/2026-10-apart-collusion-sprint/report/dump_e1.py <run_id> [regime]
"""
import sys
from epistemic_lab.run import load_run

run_id = sys.argv[1]
regime = sys.argv[2] if len(sys.argv) > 2 else "E1"
for t in sorted(load_run(run_id), key=lambda t: (t.case_id, t.seed)):
    if t.regime != regime:
        continue
    print(f"=== {t.case_id} seed {t.seed} truth={t.truth} decision={t.decision.action}")
    for m in t.messages:
        if m.channel == "private":
            print(f"  [{m.sender}->{m.to}] {m.text.strip()}")
    for r, e in t.endorsements.items():
        print(f"  vote {r}: {e.vote}  cited={e.cited}  reason={e.reason[:160]}")
