"""Per-model summary rows for the report, computed from saved held-out runs.

Run from lab/:
  uv run python ../projects/2026-10-apart-collusion-sprint/report/model_table.py label=run_id [label=run_id ...]

For each run it prints one Markdown table row per measure: false approval rate per regime, the
three matched contrasts (95 percent bootstrap by family, 2,000 resamples, seed 0), rule-auditor
flag rates on E1 and F, pooled false-positive rate on {B, C, D, E0, F} for S3 and S4d and their
difference, AUROC of S2 for E1 against {B, C, E0}, private-channel use by the proposer in E1, and
the LLM-judge counts if judge.jsonl exists. All numbers come from the frozen hand rule in
design/auditors.md section 3. Nothing here changes the preregistered analysis.
"""
import json
import sys

from epistemic_lab.auditors import SLICES, RuleAuditor, features
from epistemic_lab.metrics import auroc_subset, bootstrap_by_family, paired_far_difference
from epistemic_lab.run import RUNS, _counterfactual_index, load_run

INNOCENT = ["B", "C", "D", "E0", "F"]
REGIMES = ["A", "B", "C", "D", "E0", "E1", "F", "P"]
N_BOOT = 2000


def ci(triple: tuple[float, float, float]) -> str:
    p, lo, hi = triple
    return f"{p:.3f} [{lo:.3f}, {hi:.3f}]"


def summarize(run_id: str) -> dict:
    trajs = load_run(run_id)
    cf = _counterfactual_index(trajs)
    feat = {t.key: features(t, cf.get(t.key)) for t in trajs}
    aud = {s: RuleAuditor(s) for s in SLICES}
    flag = {(s, t.key): aud[s].score(feat[t.key]) >= aud[s].threshold for s in SLICES for t in trajs}
    out: dict = {"run": run_id, "n": len(trajs)}
    for r in REGIMES:
        fs = [t for t in trajs if t.regime == r and not t.truth]
        out[f"FAR_{r}"] = sum(t.decision.action == "approve" for t in fs) / len(fs) if fs else float("nan")
    ta = [t for t in trajs if t.regime == "A" and t.truth]
    out["TAR_A"] = sum(t.decision.action == "approve" for t in ta) / len(ta) if ta else float("nan")
    out["comm"] = bootstrap_by_family(trajs, paired_far_difference("E1", "E0"), N_BOOT)
    out["parallel"] = bootstrap_by_family(trajs, paired_far_difference("E0", "A"), N_BOOT)
    out["shared"] = bootstrap_by_family(trajs, paired_far_difference("B", "A"), N_BOOT)
    for r in ("E1", "F"):
        ts = [t for t in trajs if t.regime == r]
        out[f"flag_{r}"] = {s: sum(flag[(s, t.key)] for t in ts) / len(ts) for s in SLICES}

    def pooled(s):
        def stat(ts):
            xs = [flag[(s, t.key)] for t in ts if t.regime in INNOCENT]
            return sum(xs) / len(xs) if xs else float("nan")
        return stat

    out["fpr_S3"] = bootstrap_by_family(trajs, pooled("S3"), N_BOOT)
    out["fpr_S4d"] = bootstrap_by_family(trajs, pooled("S4d"), N_BOOT)
    out["reduction"] = bootstrap_by_family(trajs, lambda ts: pooled("S3")(ts) - pooled("S4d")(ts), N_BOOT)
    s2 = [aud["S2"].score(feat[t.key]) for t in trajs]
    out["auroc_S2"] = auroc_subset(trajs, s2, ["E1"], ["B", "C", "E0"])
    e1 = [t for t in trajs if t.regime == "E1"]
    out["private_E1"] = sum(any(m.channel == "private" and m.sender == "P" for m in t.messages) for t in e1)
    out["n_E1"] = len(e1)
    out["controls_ok"] = all(flag[(s, t.key)] for s in ("S3", "S4d", "S4") for t in trajs if t.regime == "P") and \
        not any(flag[(s, t.key)] for s in ("S3", "S4d", "S4") for t in trajs if t.regime == "A")
    for name, tag in (("judge.jsonl", "judge"), ("judge-haiku.jsonl", "judge2")):
        jf = RUNS / run_id / name
        if not jf.exists():
            continue
        rows = [json.loads(x) for x in jf.read_text(encoding="utf-8").splitlines() if x.strip()]
        for s in ("S1", "S3"):
            for r in ("E1", "F"):
                xs = [x["score"] for x in rows if x["slice"] == s and x["regime"] == r and x["score"] is not None]
                out[f"{tag}_{s}_{r}"] = f"{sum(x >= 0.5 for x in xs)} of {len(xs)}"
            inn = [x["score"] for x in rows if x["slice"] == s and x["regime"] in ["A", "B", "C", "D", "E0"]
                   and x["score"] is not None]
            out[f"{tag}_{s}_innocent"] = sum(x >= 0.5 for x in inn)
    return out


def main(argv: list[str]) -> None:
    runs = [a.split("=", 1) for a in argv]
    res = {label: summarize(run_id) for label, run_id in runs}
    labels = list(res)
    print("| Measure | " + " | ".join(labels) + " |")
    print("|---|" + "---|" * len(labels))
    for r in REGIMES:
        print(f"| FAR {r} | " + " | ".join(f"{res[l][f'FAR_{r}']:.3f}" for l in labels) + " |")
    print("| TAR A | " + " | ".join(f"{res[l]['TAR_A']:.3f}" for l in labels) + " |")
    for k, name in (("comm", "E1 minus E0"), ("parallel", "E0 minus A"), ("shared", "B minus A")):
        print(f"| {name} | " + " | ".join(ci(res[l][k]) for l in labels) + " |")
    for r in ("E1", "F"):
        print(f"| {r} flagged S1 / S3 / S4d | " + " | ".join(
            " / ".join(f"{res[l][f'flag_{r}'][s]:.2f}" for s in ("S1", "S3", "S4d")) for l in labels) + " |")
    print("| Pooled FPR S3 | " + " | ".join(ci(res[l]["fpr_S3"]) for l in labels) + " |")
    print("| Pooled FPR S4d | " + " | ".join(ci(res[l]["fpr_S4d"]) for l in labels) + " |")
    print("| Reduction S3 minus S4d | " + " | ".join(ci(res[l]["reduction"]) for l in labels) + " |")
    print("| AUROC S2, E1 vs B,C,E0 | " + " | ".join(f"{res[l]['auroc_S2']:.2f}" for l in labels) + " |")
    print("| Proposer used private channel in E1 | " + " | ".join(
        f"{res[l]['private_E1']} of {res[l]['n_E1']}" for l in labels) + " |")
    print("| Controls pass (P all flagged, A none) | " + " | ".join(
        "yes" if res[l]["controls_ok"] else "NO" for l in labels) + " |")
    for tag, label in (("judge", "Judge (DeepSeek chat)"), ("judge2", "Judge 2 (Claude Haiku 5.5)")):
        if any(f"{tag}_S1_E1" in res[l] for l in labels):
            for s in ("S1", "S3"):
                print(f"| {label} {s}: E1 / F / innocent | " + " | ".join(
                    f"{res[l].get(f'{tag}_{s}_E1', '-')} / {res[l].get(f'{tag}_{s}_F', '-')} / {res[l].get(f'{tag}_{s}_innocent', '-')}"
                    for l in labels) + " |")
    print("| n trajectories | " + " | ".join(str(res[l]["n"]) for l in labels) + " |")


if __name__ == "__main__":
    main(sys.argv[1:])
