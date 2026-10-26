---
title: "Apart AI Collusion Research Sprint, Track 2.3: epistemic plus factors"
status: draft
updated: 2026-10-23
depends_on: ["GLOSSARY.md", "hypotheses/HYPOTHESES.md", "design/regimes.md", "design/auditors.md"]
---

# Epistemic plus factors: separating collusion from correlated agreement in AI review

> **Check first (2026-10-23).** The sprint page showed "The submission window has closed"
> on the submission form while the sign-up form was open and the stated deadline is
> 2026-10-25 23:59 Anywhere on Earth (= 2026-10-26 11:59 UTC = 2026-10-26 19:59 Manila).
> Sign up on the page, join the Discord (link on the page), and ask whether the form opens.
> Do not start the report until this is answered. The experiment is worth running either way:
> it is the dataset for the TARA project.

**Track:** 2.3, "What should count as convincing evidence of collusion?" Secondary: 2.2
(say versus do). **Team:** 1 to 5 people. **Format:** PDF report, 8 pages maximum
excluding references and appendices, abstract 150 to 250 words, required appendix
"Limitations and Dual-Use / Ethical Considerations". Official template: Google Doc linked
from the sprint page. Optional: public repo, 3 to 5 minute video.

## 1. Research question

> Can an auditor that sees provenance, exposure order, payoff structure, and channel
> availability separate coordinated misleading endorsements from four innocent
> explanations of the same agreement (shared source, conformity, single-agent persuasion,
> parallel conduct) and from talk without action, more reliably than an auditor that sees
> only messages, only actions, or both?

This is a Track 2.3 question. The sprint guide asks for three case types: coordinated
harmful action, similar behavior from common incentives without agreement, and
collusive-sounding talk that never changes behavior. Our regimes E1 and P, E0, and F are
those three. Regimes B, C, and D add the explanations that social epistemology predicts.

## 2. Contribution (what is new, stated carefully)

**[HYPOTHESIS]** The contribution is a set of *epistemic plus factors*: trajectory
features drawn from provenance, exposure order, payoffs, and channel use, together with a
test of which factors discriminate collusion from each innocent explanation. The nearest
prior work:

- Nakamura et al. 2026, Colosseum [S1]: shows coalition formation and that collusive talk
  need not become collusive action. We add matched innocent regimes and a provenance layer.
- Rose et al. 2026, NARCBench [R17]: activation-based detection. We are black-box and
  evidence-based; our regimes are designed as the confound set their probes would need.
- Hu et al. 2026, Lying with Truths [R14]: truthful-fragment manipulation. Our regime D is
  the single-agent version; our provenance features are what would catch it.
- Berger et al. 2025 (sprint reading, antitrust plus factors): the legal source of the
  plus-factor idea. We operationalize it for agent trajectories.

We do **not** claim that provenance-aware auditing must win. A null result (S4 adds nothing
over S3) is a valid finding and is written up with the same rigor.

## 3. Design in one table

| Element | Choice | Where specified |
|---|---|---|
| Environment | Proposer-reviewer-decider review game; claims with ground truth; evidence items with provenance | `design/game.md` |
| Cases | 12 case families x 2 truth values = 24 cases (pilot: 6 families) | `design/game.md`, `lab/configs/` |
| Regimes | A, B, C, D, E0, E1, F, P (8) | `design/regimes.md` |
| Agents | Scripted (positive and negative controls) and one small LLM via OpenAI-compatible adapter | `lab/src/epistemic_lab/agents.py` |
| Auditors | 5 information slices (S1, S2, S3, S4d primary, S4 exploratory) x 2 implementations (rule-based plus factors; LLM judge) | `design/auditors.md` |
| Primary measures | Per-regime flag rate; false-positive rate on {B, C, D, E0, F}; recall on {E1, P}; AUROC; all against both the regime label and the behavioral collusion label | `design/auditors.md` |
| Decision harm | False approval rate, true approval rate, deferral rate per regime; Δ_comm = E1 − E0 | `design/regimes.md` |
| Split | Dev 6 families, held-out 6 families; decision rule frozen on dev | `PREREGISTRATION.md` |
| Seeds | 1 per cell in pilot; 3 per cell in main run if budget allows | `PLAN.md` |
| Budget | USD 2 to 15 total | `PLAN.md` |

## 4. Hypotheses (ids in `hypotheses/HYPOTHESES.md`)

| Id | Short statement | Falsifier |
|---|---|---|
| H-SPRINT-1 | Messages-only auditors cannot separate talk without action (F) from collusion (E1). | FPR on F under S1 is below half of recall on E1 under S1. |
| H-SPRINT-2 | Actions-only auditors cannot separate harmful correlated agreement (B, C, E0) from collusion (E1). | AUROC of S2 for E1 versus {B, C, E0} exceeds 0.80. |
| H-SPRINT-3 | Adding provenance, exposure order, private evidence, and the channel-off counterfactual (S4d, no payoff knowledge) lowers false-positive rate on innocent regimes relative to S3 while recall on E1 stays within S3's bootstrap interval. Full S4 with payoffs is exploratory only (CF-13). | No FPR reduction, or recall falls outside the interval. |
| H-SPRINT-4 | The communication effect Δ_comm = P(invalid approval \| E1) − P(invalid approval \| E0) is positive with a 95 percent bootstrap interval excluding zero; the matched quantity with accuracy-aligned payoffs (F − A) is not. | Interval for E1 − E0 includes zero. |
| H-SPRINT-5 | Parallel conduct (E0) produces invalid approvals above the A baseline: harm without agreement exists. | E0 false approval rate is not above A's. |

## 5. Timeline (owner is in UTC+8; deadline is 2026-10-26 19:59 Manila)

See `PLAN.md` for the hour-by-hour version. Summary:

| Date | Deliverable |
|---|---|
| 2026-10-23 (Fri) | Scaffold; positive control detected; regimes and auditors specified; preregistration drafted |
| 2026-10-24 (Sat) | Freeze preregistration; pilot 6 families x 8 regimes with LLM; inspect every trajectory; fix prompts; run dev families |
| 2026-10-25 (Sun) | Run held-out families; compute metrics with intervals; write report; limitations appendix; repo README with preexisting-work disclosure |
| 2026-10-26 (Mon, before 19:59) | Final read; submit |

## 5b. Scripted demo result (2026-10-23, zero API cost) [FINDING, scripted agents only]

`uv run elab demo --seeds 5` on 12 families x 2 truths x 5 seeds x 8 regimes (960 trajectories):

| Regime | FAR | TAR | behavioral label rate | S1 flag | S2 flag | S3 flag | S4d flag | S4 flag |
|---|---|---|---|---|---|---|---|---|
| A | 0.017 | 0.733 | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 |
| B | 0.167 | 0.833 | 0.00 | 0.00 | 0.08 | 0.00 | 0.00 | 0.00 |
| C | 0.033 | 0.800 | 0.00 | 0.00 | 0.02 | 0.00 | 0.00 | 0.00 |
| D | 0.167 | 0.917 | 0.00 | 0.00 | 0.08 | 0.00 | 0.00 | 0.00 |
| E0 | 0.567 | 1.000 | 0.00 | 0.00 | 0.28 | 0.00 | 0.00 | 0.00 |
| F | 0.017 | 0.733 | 0.30 | 1.00 | 0.01 | 0.38 | 0.30 | 0.00 |
| P | 0.567 | 1.000 | 1.00 | 1.00 | 0.28 | 1.00 | 1.00 | 1.00 |

The S4 column is perfect because payoff knowledge identifies the regime (CF-13); it is not
the contribution. S4d, which a deployer could compute, flags the 30 percent of F trajectories
in which the injected plan coincided with the votes, and those are exactly the trajectories
the behavioral label also marks. Separating them needs hand adjudication or a better f9.

Paired contrasts on false claims, 95 percent bootstrap by family: E0 − A = 0.550 [0.486, 0.613];
B − A = 0.150 [0.086, 0.200]; Δ_comm (P as E1) − E0 = 0.000; F − A = 0.000.

What this shows: the pipeline works; the positive control is flagged by S3, S4d, and S4 and
the negative control is not; S1 is fooled by F; S2 cannot separate E0 from P; shared source and
parallel conduct each raise false approvals without any coordination. What this does not
show: anything about language models. These agents follow rules we wrote.

## 6. Preexisting work disclosure (required by sprint rules)

- The 2026-10-20 research starter (`archive/`) is a scoping document written before the
  sprint. No code from it.
- Concepts "claim versus accepted fact", "source lineage", "review decision as a separate
  act" come from the owner's prior Grid Nowcast ontology work. No Grid Nowcast code is
  used. The sprint code in `lab/` is new as of 2026-10-23.
- The repository scaffold (`lab/` skeleton, `bayes.py`, scripted game) was written on
  2026-10-23, the first sprint day, with AI assistance. State this in the report README.

## 7. Files in this folder

| File | Purpose |
|---|---|
| `README.md` | This brief. |
| `PLAN.md` | Hour-by-hour execution plan, budget, stop rules. |
| `PREREGISTRATION.md` | Hypotheses, predictions, falsifiers, analysis plan. Freeze before the first LLM run. |
| `design/game.md` | The review game: roles, information, actions, payoffs, logging schema. |
| `design/regimes.md` | The eight regimes as factor settings; what each isolates. |
| `design/auditors.md` | Information slices, plus-factor features, decision rule, metrics. |
| `report/OUTLINE.md` | Report skeleton in the Apart structure with page budget. |
| `report/LIMITATIONS.md` | Running list for the required appendix. |
