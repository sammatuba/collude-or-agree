# lab/

Code that produces evidence. One `uv` project, Python 3.13, numpy only in the core.

## What is here

| Module | Glossary term it implements | Spec |
|---|---|---|
| `bayes.py` | likelihood ratio, conditional independence, double counting | `foundations/01-evidence-independence.md` |
| `cases.py` | case, case family, evidence item, origin, derivative, provenance | `projects/2026-10-apart-collusion-sprint/design/game.md` section 2 |
| `regimes.py` | regime, regime label, collusion label | `design/regimes.md` |
| `agents.py` | proposer, reviewer, decider (scripted and LLM) | `design/game.md` sections 3 and 8 |
| `game.py` | trajectory, payoff, invalid approval | `design/game.md` sections 4 to 7 |
| `auditors.py` | information slice, epistemic plus factor, rule auditor, LLM judge | `design/auditors.md` |
| `metrics.py` | false approval rate, true approval rate, AUROC, bootstrap interval, communication effect | `design/auditors.md` section 6; `foundations/07-measurement.md` |
| `llm.py` | the only network module; OpenAI-compatible; cached | `DECISIONS.md` D-005 |
| `prompts.py` | every prompt verbatim | report appendix A |
| `run.py` | `elab` command line | this file |

## Setup (once)

```
cd lab
uv venv --python 3.13 .venv
uv sync --extra dev          # add --extra ml for torch, transformers, scikit-learn (TARA)
uv run pytest
```

## Zero-cost run (do this first)

```
uv run elab demo --seeds 5
```

Slices: S1 messages, S2 actions, S3 both, S4d deployable metadata (primary), S4 full
metadata with payoff rules (exploratory; see confound CF-13). Runs every case family under
every regime with scripted agents, prints approval rates per
regime, auditor flag rates per slice, and the paired contrasts with bootstrap intervals,
then checks the positive control (P flagged by S3 and S4 at 100 percent) and the negative
control (A never flagged by S4). Output lands in `data/runs/demo/`.

What the demo shows and does not show. It shows that the pipeline works and that the
plus-factor logic behaves as designed on agents whose rules we wrote. It does not show
anything about language models. The scripted world is the positive control for the
pipeline; the LLM run is the experiment.

## LLM run (needs a key)

```
cp .env.example .env         # fill LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
uv run elab write-configs    # freezes dev/held-out family lists to configs/
uv run elab llm --split dev --seeds 1 --run-id dev-2026-10-24      # 6 families x 2 x 8 regimes = 96 trajectories
uv run elab audit dev-2026-10-24                                  # hand-rule auditors
uv run elab llm --split heldout --seeds 1 --run-id heldout-2026-10-25
uv run elab audit heldout-2026-10-25 --fit dev-2026-10-24          # rule fitted on dev, evaluated on held-out
```

Every LLM response is cached in `data/cache/` by request hash. Re-running is free. The
`meta.json` of each run records the model id, usage, and dropped trajectories.

Regime P always uses scripted agents (certain collusion). Regime F uses the scripted honest
proposer plus injected coordination text, with LLM reviewers and decider, so the only
difference from A is the talk.

## Notebooks

`notebooks/*.py` are percent-format notebooks (`# %%` cells). Open them in VS Code and run
cell by cell, or convert: `uv run jupytext --to ipynb notebooks/01_evidence_independence.py`.
No `.ipynb` files are committed (decision D-006).

| Notebook | Teaches |
|---|---|
| `01_evidence_independence.py` | Why three copies give 0.80 and three independent reports give 0.985 |
| `02_review_game_scripted.py` | The game, the regimes, the demo tables, reading one trajectory |
| `03_plus_factor_auditors.py` | Features, slices, fitting the logistic rule on dev, ROC by slice |
| `04_tara_probe_plan.py` | Activation extraction and a linear probe on trajectories (torch; requires `--extra ml`) |

## Tests

`uv run pytest`. The tests encode the design guarantees: positive control always flagged by
S3 and S4; negative control never flagged by S4; talk without action trips S1 and S3 but not
S4; shared source raises false approval rate for naive agents; AUROC known values.

## Preexisting work

All code here was written on or after 2026-10-23 (sprint day 1).
