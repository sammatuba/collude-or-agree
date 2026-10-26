"""Print one case under every regime, compactly, for learning by hand.

Run from lab/:
  uv run python ../projects/2026-10-apart-collusion-sprint/report/trace.py F03-F 0
  uv run python ../projects/2026-10-apart-collusion-sprint/report/trace.py F03-F 0 --answers

Arguments: case id (family + -T or -F), seed. Without --answers it prints only what you need
to work the exercises (evidence, messages, endorsements, decision). With --answers it also
prints the plus-factor features and the hand-rule score per information slice.
Needs: uv run elab demo --seeds 5 --boot 2000  (writes lab/data/runs/demo).
"""
import sys

from epistemic_lab.auditors import SLICES, behavioral_collusion_auto, features, hand_rule
from epistemic_lab.run import _counterfactual_index, load_run

case_id, seed = sys.argv[1], int(sys.argv[2])
answers = "--answers" in sys.argv
trajs = load_run("demo")
cf = _counterfactual_index(trajs)
sel = [t for t in trajs if t.case_id == case_id and t.seed == seed]
if not sel:
    sys.exit(f"no trajectories for {case_id} seed {seed}")

t0 = sel[0]
print(f"CASE {case_id} seed {seed}   ground truth: {'TRUE' if t0.truth else 'FALSE'}")
print(f"claim: {t0.claim.text}\n")
for t in sorted(sel, key=lambda t: ["A", "B", "C", "D", "E0", "E1", "F", "P"].index(t.regime)):
    rf = t.regime_factors
    print(f"=== regime {t.regime}: provenance={rf.provenance} exposure={rf.exposure} "
          f"channel={rf.channel} payoff_P={rf.payoff_P} payoff_R={rf.payoff_R}")
    print("  agents:", ", ".join(f"{k}={v.split(':')[-1]}" for k, v in t.agents.items()))
    print("  evidence (id origin parent reports):")
    for e in t.evidence:
        print(f"    {e.id:3s} {e.origin:3s} {str(e.parent):5s} {'TRUE ' if e.reports_true else 'FALSE'}")
    print(f"  presented: {t.presented}   private slices: {t.private_slices}")
    for m in t.messages:
        print(f"  msg {m.sender}->{m.to} [{m.channel}]: {m.text}")
    for k, e in t.endorsements.items():
        print(f"  {k}: {e.vote:7s} cites {e.cited}")
    print(f"  decider: {t.decision.action}   invalid approval: {t.invalid_approval}")
    if answers:
        f = features(t, cf.get(t.key))
        keys = ["agree", "invalid", "coord_talk", "private_used", "followed_plan", "shared_origin",
                "exposure", "payoff_aligned", "against_evidence", "cf_shift"]
        print("  features:", " ".join(f"{k}={f[k]:.2g}" for k in keys))
        print("  scores:  ", " ".join(f"{s}={hand_rule(s, f):.2f}" for s in SLICES),
              f"  behavioral label={behavioral_collusion_auto(f)}")
    print()
