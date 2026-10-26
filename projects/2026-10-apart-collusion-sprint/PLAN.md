---
title: "Sprint execution plan"
status: draft
updated: 2026-10-23
depends_on: ["README.md", "PREREGISTRATION.md"]
---

# Sprint execution plan

Tool-agnostic. Each step names its input file, its output file, and its check. Do the
steps in order. If a step fails its check, stop and log in `STATUS.md`.

## Stop rules

- Do not spend API credit before `PREREGISTRATION.md` has `frozen_on` set.
- Do not run the held-out families until the decision rule is written in
  `design/auditors.md` section 5 and the dev results are logged.
- If by 2026-10-25 12:00 Manila the LLM regimes do not separate (all regimes give the same
  approval rates within noise), switch the report to the scripted-agent study plus the
  Bayesian analysis, and state that LLM behavior under these prompts was not separable.

## Budget

| Line | Calls | Est. tokens | Est. cost (USD) |
|---|---|---|---|
| Pilot: 6 families x 2 truths x 8 regimes = 96 trajectories, about 5 calls each | 480 | 0.7M | 0.5 to 2 |
| Main: 12 families x 2 x 8 = 192 trajectories x 1 seed | 960 | 1.4M | 1 to 4 |
| Extra seeds (optional): x2 more | 1920 | 2.8M | 2 to 8 |
| LLM-judge auditors: 192 x 2 slices (S3, S4) | 384 | 0.6M | 0.5 to 2 |
| **Total** | | | **2 to 15** |

**Budget line added 2026-10-26 (owner approved a capped budget).** OpenRouter replication on the
held-out split, 3 seeds, 252 language-model trajectories per model: `anthropic/claude-haiku-5.5`
(USD 0.10 / 0.50 per million input / output tokens) and `openai/gpt-5.6-luna` (USD 0.20 / 1.20),
prices from the OpenRouter model list on 2026-10-26. Estimate about USD 0.05 and 0.15. **Hard cap:
USD 2.00 total**, set as the credit limit on the OpenRouter key itself. DeepSeek main run actual
usage: about 0.74M input and 0.12M output tokens (agents), plus 0.24M and 0.07M (judge).

**Budget line added 2026-10-26 (owner approved in the session): OpenRouter, more models, USD 10.00
new spend.** The owner deferred Modal (no time; Modal sells GPU time, not model endpoints). Scope:
the held-out split (families F07 to F12), 3 seeds, all regimes, 252 language-model trajectories
per model, P scripted. Same prompts, `LLM_MAX_TOKENS=1500`. Exploratory (PREREGISTRATION amendment).
Prices from the OpenRouter model list fetched 2026-10-26 (USD per million input / output tokens).
Per-run token estimates come from the Haiku run (0.59M input, 0.32M output for 288 trajectories)
and the Luna run (0.35M, 0.18M). Key usage before this line: USD 0.545 (key limit USD 20).

| Order | Model | Price in / out | Estimate (USD) | Gate |
|---|---|---|---|---|
| 1 | `deepseek/deepseek-v4-flash` | 0.09 / 0.18 | 0.1 | **dropped**: smoke test returned empty replies in 2 of 4 trajectories |
| 2 | `deepseek/deepseek-v4-pro` | 0.96 / 1.91 | 1.3 | **stopped** two minutes after launch; moved to the DeepSeek platform line below |
| 3 | `anthropic/claude-sonnet-5.5` | 2.00 / 10.00 | 4.7 | smoke test passes |
| 4 | `openai/gpt-5.6-terra` | 2.00 / 12.00 | 3.2 to 5.4 | measured spend after 1 to 3 leaves room; else 2 seeds |
| | **Hard cap** | | **10.00** | a monitor reads the key's usage counter every minute and stops the runs at 9.7 new spend |

Smoke tests on 2026-10-26 (family F07, 1 seed, regimes E1 and F, 4 trajectories): all four models cost USD 0.154 together. Scaled to 252 trajectories: Sonnet 5.5 about 4.2 to 4.8, Terra about 2.9 to 3.3, DeepSeek V4 Pro about 1.5. All three were launched in parallel at 15:25 Manila time (UTC+8), 18 processes. **Actual spend (key usage counter, 2026-10-26 after all runs and refills): USD 5.08 of the 10.00 line** (Sonnet 5.5, Terra, four smoke tests, and the stopped V4 Pro jobs). DeepSeek platform line: balance fell from USD 26.29 to 25.20 (USD 1.09, which includes the four LLM-judge runs on `deepseek-chat`).

**Budget line added 2026-10-26 (owner: DeepSeek models use the DeepSeek platform key, outside the
USD 10 OpenRouter line).** The platform lists `deepseek-v4-pro` and `deepseek-flash` (model list
fetched 2026-10-26; balance USD 26.29). Scope as above (held-out, 3 seeds, 252 trajectories per
model), `LLM_ENV_FILE=lab/.env`, thinking disabled (both models think by default; see PREREGISTRATION amendments). Estimate: V4 Pro about USD 1.5 (reasoning output), Flash under 0.5.
**Cap for this line: USD 5.00** of the DeepSeek balance. The OpenRouter `deepseek/deepseek-v4-pro`
jobs were stopped two minutes after launch (cost: cents) when the owner gave this instruction.

Not affordable at full scope within this line: `anthropic/claude-opus-5.5` (4 / 20, about USD 9.4)
and `openai/gpt-5.6-sol` (4 / 20, about 5.6 to 9.4). A 1-seed run of one of them (about USD 3)
needs a new owner decision.

**Budget lines added 2026-10-26 (owner: "go ahead with all three").**
- **Second judge model.** The exploratory LLM judge re-run with `anthropic/claude-haiku-5.5` through
  OpenRouter on all seven held-out runs (7 x 576 calls). Estimate about USD 0.5. **Cap USD 1.00.**
  Output goes to `judge-haiku.jsonl` in each run folder; the DeepSeek judge file is kept.
- **Coordination-pivotal regimes E0p and E1p.** Same as E0 and E1, but a reviewer who endorses an
  approved false claim alone is blamed (-2 on top of +1, so -1 net); if both endorse, nobody is blamed. Held-out families,
  3 seeds, 72 trajectories per model: GPT-5.6 Terra (OpenRouter, about USD 1), DeepSeek chat and
  DeepSeek Flash (DeepSeek platform, cents). **Cap USD 3.00 OpenRouter, USD 1.00 DeepSeek platform.**
  Smoke test first (one family, one seed).
  Added after E1p: regime E1q (the proposer knows the reviewers' rule), 36 trajectories per model, same
  three models, inside the same caps. Actual E0p/E1p spend: Terra about USD 0.9; DeepSeek models cents.

Model: one small instruction model via OpenRouter or Nebius (set `LLM_MODEL` in
`lab/.env`). Record the exact model id, temperature (0.2 for agents, 0 for judges), and date
in `lab/data/runs/<run_id>/meta.json`.

## 2026-10-23 (Friday)

| Step | Input | Output | Check |
|---|---|---|---|
| F1 Read the brief, regimes, auditors | this folder | understanding | You can state the three sprint case types and which regime is each. |
| F2 Set up lab | `lab/README.md` | `lab/.venv` | `uv run pytest` passes. |
| F3 Run scripted demo | `lab/src/epistemic_lab/run.py --demo` | console table | Positive control P flagged by rule auditor at S3 and S4; negative control A not flagged. |
| F4 Read Bayesian demo | `lab/notebooks/01_evidence_independence.py` | your note in `study/notes/` | You can explain why three copies give 80 percent, not 98.5 percent. |
| F5 Sign up; Discord; confirm form status | sprint page | `STATUS.md` entry | Written answer: open or closed. |
| F6 Draft preregistration | `PREREGISTRATION.md` | filled tables | Every hypothesis has a number or direction and a falsifier. |

## 2026-10-24 (Saturday)

| Step | Input | Output | Check |
|---|---|---|---|
| S1 Set `lab/.env`; smoke test one LLM call | `lab/README.md` | cached response | One trajectory under regime A completes and logs. |
| S2 Freeze preregistration | `PREREGISTRATION.md` | `frozen_on: 2026-10-24` | No further edits except the Amendments table. |
| S3 Pilot: 6 dev families x 8 regimes | `lab/configs/cases_dev.json` | `lab/data/runs/pilot/` | 96 trajectories; read 16 by hand (2 per regime); log failure categories. |
| S4 Fix prompts only for parse failures | pilot logs | amended prompts | Record every change in Amendments. Do not tune toward the hypothesis. |
| S5 Dev run (re-run 6 dev families if prompts changed) | configs | `lab/data/runs/dev/` | Approval rates per regime table. |
| S6 Fit and freeze decision rule on dev | `auditors.py` | `design/auditors.md` section 5 | Threshold or logistic weights written with date. |
| S7 Compute dev metrics | `metrics.py` | `report/tables/dev.md` | Per-regime flag rate; FPR; recall; AUROC; intervals. |

## 2026-10-25 (Sunday)

| Step | Input | Output | Check |
|---|---|---|---|
| U1 Held-out run: 6 families x 8 regimes | configs | `lab/data/runs/heldout/` | 96 trajectories. |
| U2 Held-out metrics with bootstrap by family | `metrics.py` | `report/tables/heldout.md` | Each hypothesis marked supported, refuted, or inconclusive. |
| U3 Δ_comm and matched aligned contrast | `metrics.py` | table | Intervals reported. |
| U4 Error analysis: every false positive and miss under S4 | logs | `report/ERRORS.md` | Each assigned a failure category from the glossary. |
| U5 Write report | `report/OUTLINE.md` | PDF via template | 8 pages; abstract 150 to 250 words; positive control reported; variance reported. |
| U6 Limitations and dual-use appendix | `report/LIMITATIONS.md` | appendix | Covers prompt-conditioned behavior, single model, synthetic cases, dual use of plus factors. |
| U7 Public repo | `lab/` | GitHub | README marks preexisting work; run instructions reproduce one figure. |

## 2026-10-26 (Monday, before 19:59 Manila)

| Step | Check |
|---|---|
| M1 Re-read against judging criteria: impact and innovation, execution quality, presentation | Each criterion has one paragraph that answers it. |
| M2 Submit; save confirmation | `STATUS.md` entry with time. |

## Division of labor if a team forms

| Role | Owns |
|---|---|
| Environment | `game.py`, `cases.py`, configs |
| Agents and prompts | `agents.py`, `llm.py`, prompt files |
| Auditors and metrics | `auditors.py`, `metrics.py`, tables |
| Report | `report/`, figures, limitations |
