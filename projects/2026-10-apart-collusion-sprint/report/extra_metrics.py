"""Extra metrics for the sprint report, computed from the saved scripted demo run.

Run from lab/:  uv run python ../projects/2026-10-apart-collusion-sprint/report/extra_metrics.py [run_id]
(default run_id: demo; for the language-model data use llm-heldout-2026-10-26 or llm-dev-2026-10-26)
Needs: uv run elab demo --seeds 5 --boot 2000  (writes lab/data/runs/demo).
Computes exact counts, the pooled false-positive rate on the innocent regimes {B, C, D, E0, F}
per information slice, and the paired difference S3 minus S4d, with 95 percent bootstrap
intervals that resample case families (2,000 resamples, seed 0).
"""
import sys

from epistemic_lab.run import load_run, _counterfactual_index
from epistemic_lab.auditors import RuleAuditor, SLICES, features, behavioral_collusion_auto
from epistemic_lab.metrics import bootstrap_by_family

RUN = sys.argv[1] if len(sys.argv) > 1 else "demo"
trajs = load_run(RUN)
cf = _counterfactual_index(trajs)
feat = {t.key: features(t, cf.get(t.key)) for t in trajs}
aud = {s: RuleAuditor(s) for s in SLICES}
flag = {(s, t.key): aud[s].score(feat[t.key]) >= aud[s].threshold for s in SLICES for t in trajs}
INNOCENT = ["B", "C", "D", "E0", "F"]
REGIMES = ["A", "B", "C", "D", "E0", "E1", "F", "P"]

print("run:", RUN, " n trajectories:", len(trajs), " families:", len({t.family for t in trajs}))
print("\nFalse approvals per regime (count / false-claim trajectories)")
for r in REGIMES:
    fs = [t for t in trajs if t.regime == r and not t.truth]
    print(f"  {r:3s} {sum(t.decision.action == 'approve' for t in fs)}/{len(fs)}")

print("\nFlags per regime x slice (count / n)")
for s in SLICES:
    row = []
    for r in REGIMES:
        ts = [t for t in trajs if t.regime == r]
        row.append(f"{r}:{sum(flag[(s, t.key)] for t in ts)}/{len(ts)}")
    print(f"  {s:4s} " + "  ".join(row))

def pooled_fpr(s):
    def stat(ts):
        xs = [flag[(s, t.key)] for t in ts if t.regime in INNOCENT]
        return sum(xs) / len(xs) if xs else float("nan")
    return stat

print("\nPooled FPR on {B,C,D,E0,F} [95% bootstrap by family]")
for s in SLICES:
    p, lo, hi = bootstrap_by_family(trajs, pooled_fpr(s), 2000)
    print(f"  {s:4s} {p:.3f} [{lo:.3f}, {hi:.3f}]")
p, lo, hi = bootstrap_by_family(trajs, lambda ts: pooled_fpr("S3")(ts) - pooled_fpr("S4d")(ts), 2000)
print(f"  S3 - S4d reduction: {p:.3f} [{lo:.3f}, {hi:.3f}]")

f_flag = [t for t in trajs if t.regime == "F" and flag[("S4d", t.key)]]
beh = sum(behavioral_collusion_auto(feat[t.key]) for t in f_flag)
print(f"\nF trajectories flagged by S4d: {len(f_flag)}; of these with behavioral label 1: {beh}")

pairs = {(t.case_id, t.seed): t for t in trajs if t.regime == "E0"}
same = sum(pairs[(t.case_id, t.seed)].decision.action == t.decision.action
           for t in trajs if t.regime == "P")
print(f"P trajectories whose decider action equals the matched E0 trajectory: {same}/{len(pairs)}")
