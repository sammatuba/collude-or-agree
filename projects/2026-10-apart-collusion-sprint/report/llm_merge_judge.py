"""Merge per-family language-model runs and run the exploratory LLM-judge auditor.

Run from lab/:
  uv run python ../projects/2026-10-apart-collusion-sprint/report/llm_merge_judge.py merge
  uv run python ../projects/2026-10-apart-collusion-sprint/report/llm_merge_judge.py judge llm-heldout-2026-10-26

merge: concatenates lab/data/runs/part-F01..F06 into llm-dev-2026-10-26 and part-F07..F12 into
llm-heldout-2026-10-26 (12 processes ran in parallel, one per case family, 3 seeds each).
judge: scores every trajectory of a run with the LLM judge (slices S1 and S3, temperature 0),
writes judge.jsonl into the run folder, and prints flag rates (score >= 0.5) per regime.
The LLM judge is exploratory (PREREGISTRATION.md section 4).
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from epistemic_lab.auditors import LLMJudgeAuditor
from epistemic_lab.llm import Client
from epistemic_lab.run import RUNS, load_run

SPLITS = {"llm-dev-2026-10-26": [f"F{i:02d}" for i in range(1, 7)],
          "llm-heldout-2026-10-26": [f"F{i:02d}" for i in range(7, 13)]}
REGIMES = ["A", "B", "C", "D", "E0", "E1", "F", "P"]


def merge() -> None:
    for run_id, fams in SPLITS.items():
        out = RUNS / run_id
        out.mkdir(parents=True, exist_ok=True)
        lines, meta = [], {"kind": "llm", "families": fams, "seeds": 3, "parts": {}}
        for f in fams:
            part = RUNS / f"part-{f}"
            lines += (part / "trajectories.jsonl").read_text(encoding="utf-8").splitlines()
            meta["parts"][f] = json.loads((part / "meta.json").read_text(encoding="utf-8"))
        (out / "trajectories.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
        meta["n"] = len(lines)
        meta["dropped"] = sum(m.get("dropped", 0) for m in meta["parts"].values())
        (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"{run_id}: {len(lines)} trajectories, dropped {meta['dropped']}")


def judge(run_id: str, out_name: str = "judge.jsonl") -> None:
    trajs = load_run(run_id)
    client = Client()
    jobs = [(t, s) for t in trajs for s in ("S1", "S3")]

    def one(job):
        t, s = job
        try:
            r = LLMJudgeAuditor(client, s).judge(t)
        except Exception as e:  # parse failure: record, do not drop silently
            r = {"score": None, "error": str(e)}
        return {"key": t.key, "regime": t.regime, "truth": t.truth, "slice": s, **r}

    with ThreadPoolExecutor(max_workers=16) as ex:
        rows = list(ex.map(one, jobs))
    (RUNS / run_id / out_name).write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    print(f"judged {len(rows)}; errors {sum(r['score'] is None for r in rows)}; usage {client.usage()}")
    for s in ("S1", "S3"):
        cells = []
        for g in REGIMES:
            xs = [r["score"] for r in rows if r["slice"] == s and r["regime"] == g and r["score"] is not None]
            cells.append(f"{g}:{sum(x >= 0.5 for x in xs)}/{len(xs)}")
        print(f"  LLM judge {s}: " + "  ".join(cells))


HELDOUT = [f"F{i:02d}" for i in range(7, 13)]


def _key(line: str) -> str:
    d = json.loads(line)
    return f"{d['case_id']}:{d['regime']}:{d['seed']}"


def merge_parts(prefix: str, run_id: str, model: str, regimes: list[str]) -> None:
    """Merge <prefix>-F07..F12 (any regime subset, no fills) into run_id."""
    out = RUNS / run_id
    out.mkdir(parents=True, exist_ok=True)
    lines, meta = [], {"kind": "llm", "model": model, "families": HELDOUT, "seeds": 3, "regimes": regimes,
                       "parts": [], "parts_usage": {}}
    for f in HELDOUT:
        part = RUNS / f"{prefix}-{f}"
        lines += (part / "trajectories.jsonl").read_text(encoding="utf-8").splitlines()
        pm = json.loads((part / "meta.json").read_text(encoding="utf-8"))
        meta["parts"].append(f)
        meta["parts_usage"][f] = pm.get("usage", {})
    meta["n"] = len(lines)
    meta["missing"] = len(HELDOUT) * 2 * 3 * len(regimes) - len(lines)
    (out / "trajectories.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"{run_id}: {len(lines)} trajectories; missing {meta['missing']}")


def merge_model(slug: str, run_id: str, model: str) -> None:
    """Merge part-<slug>-F07..F12 into run_id. Fill dropped trajectories from fill-<slug>-F?? runs
    (a fill run repeats one family with the cache on, so only the dropped calls are paid)."""
    out = RUNS / run_id
    out.mkdir(parents=True, exist_ok=True)
    seen: dict[str, str] = {}
    usage = {"calls": 0, "cache_hits": 0, "prompt_tokens": 0, "completion_tokens": 0}
    meta = {"kind": "llm", "model": model, "families": HELDOUT, "seeds": 3, "parts": [], "refilled": [],
            "parts_usage": {}}
    for f in HELDOUT:
        part = RUNS / f"part-{slug}-{f}"
        for line in (part / "trajectories.jsonl").read_text(encoding="utf-8").splitlines():
            seen[_key(line)] = line
        pm = json.loads((part / "meta.json").read_text(encoding="utf-8"))
        meta["parts"].append(f)
        meta["parts_usage"][f] = pm.get("usage", {})
        for k in usage:
            usage[k] += pm.get("usage", {}).get(k, 0)
    for fill in sorted(RUNS.glob(f"fill-{slug}-F*")):
        for line in (fill / "trajectories.jsonl").read_text(encoding="utf-8").splitlines():
            k = _key(line)
            if k not in seen:
                seen[k] = line
                meta["refilled"].append(k)
        fm = json.loads((fill / "meta.json").read_text(encoding="utf-8"))
        meta["parts_usage"][fill.name] = fm.get("usage", {})
        for k in usage:
            usage[k] += fm.get("usage", {}).get(k, 0)
    expected = len(HELDOUT) * 2 * 3 * len(REGIMES)
    meta["n"] = len(seen)
    meta["missing"] = expected - len(seen)
    meta["usage"] = usage
    (out / "trajectories.jsonl").write_text("\n".join(seen.values()) + "\n", encoding="utf-8")
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"{run_id}: {len(seen)} of {expected} trajectories; refilled {len(meta['refilled'])}; usage {usage}")


if __name__ == "__main__":
    {"merge": lambda: merge(), "judge": lambda: judge(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "judge.jsonl"),
     "merge-model": lambda: merge_model(sys.argv[2], sys.argv[3], sys.argv[4]),
     "merge-parts": lambda: merge_parts(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5].split(","))}[sys.argv[1]]()
