---
title: "Reading list, soundness review, and questions for an expert"
status: draft
updated: 2026-10-26
depends_on: ["REPORT.md", "../../../literature/INDEX.md"]
---

# Reading list, soundness review, and questions for an expert

Written for the owner on 2026-10-26, after the seven-model runs. Three parts: the papers
behind the related-work section, an assessment of how sound the work is, and questions to
bring to an AI safety expert.

## 1. The papers, in reading order

Read the first four closely. They are the direct neighbors of this project. Each line gives
the id from `literature/INDEX.md`, the link, and why it matters for this work.

| Order | Id | Work | Link | Why it matters here |
|---|---|---|---|---|
| 1 | [S1] | Nakamura et al. 2026. Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems. | https://arxiv.org/abs/2602.15198 | The closest prior work. It reports "collusion on paper": agents agree in text and do not act. Our say-do gap is the same finding, measured with matched innocent regimes. |
| 2 | [R12] | Motwani et al. 2024. Secret Collusion among AI Agents. NeurIPS 2024. | https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html | The standard definition of AI collusion and the threat model where messages are hidden from the monitor. Our auditor sees all messages, so we study the easier case. |
| 3 | [R11] | Greenblatt et al. 2024. AI Control: Improving Safety Despite Intentional Subversion. ICML 2024. | https://proceedings.mlr.press/v235/greenblatt24a.html | The framing of oversight with untrusted agents. Our decider is the oversight step. Our auditor acts after the decision, which is the weaker position. |
| 4 | [S2] | Berger et al. 2025. ABA Antitrust Law magazine, Fall 2025 (plus factors and AI pricing). | https://www.americanbar.org/groups/antitrust_law/resources/magazine/2025-fall/coordination-code-rethinking-antitrust-liability-age-ai-pricing/ | Where "plus factors" come from. It is on the sprint reading list for question 2.3. Our features are plus factors turned into checks on agent records. |
| 5 | [R17] | Rose et al. 2026. Detecting Multi-Agent Collusion Through Multi-Agent Interpretability (NARCBench). | https://arxiv.org/abs/2604.01151 | Detection from internal activations. Our innocent regimes are the confounds that any such method must also pass. |
| 6 | [R14] | Hu et al. 2026. Lying with Truths: Open-Channel Multi-Agent Collusion for Belief Manipulation. ACL 2026. | https://aclanthology.org/2026.acl-long.270/ | True evidence, selected to mislead. Our regime D is the one-agent form. |
| 7 | [R15] | Okawa 2026. Emergence of Biased Consensus in Multi-Agent LLM Debates. ICML 2026. | https://proceedings.mlr.press/v306/okawa26a.html | Why a second reviewer copies a first. The basis of regime C. |
| 8 | [R6] | Bikhchandani, Hirshleifer, Welch 1992. Informational cascades. J. Political Economy. | https://doi.org/10.1086/261849 | The classic theory of conformity without collusion. Read the first ten pages. |
| 9 | [R7] | Crawford and Sobel 1982. Strategic Information Transmission. Econometrica. | https://doi.org/10.2307/1913390 | Cheap talk: when a message from a sender with its own interest carries information. The basis of regime D and of "talk without action". |
| 10 | [R8] | Kamenica and Gentzkow 2011. Bayesian Persuasion. AER. | https://doi.org/10.1257/aer.101.6.2590 | Selective disclosure as a formal model. Read the introduction and the example. |
| 11 | [S40] | Bell Atlantic v. Twombly, 550 U.S. 544 (2007). | https://www.law.cornell.edu/supct/html/05-1126.ZO.html | Parallel conduct alone does not show agreement. The legal form of regime E0. |
| 12 | [S41] | Interstate Circuit v. United States, 306 U.S. 208 (1939). | https://www.law.cornell.edu/supremecourt/text/306/208 | One letter known to reach all, then uniform action. The legal form of regime E1. |
| 13 | [S42] | Eturas and Others, CJEU C-74/14 (2016). | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62014CJ0074 | Paragraphs 39 to 49: a recipient of a collusive message can rebut participation by objecting or acting against it. The legal form of regime F and of a reviewer's refusal. |
| 14 | [S46] | Gibson v. Cendyn Group, 9th Cir. 2025. | https://cdn.ca9.uscourts.gov/datastore/opinions/2025/08/15/24-3576.pdf | Same software without pooled data is not an agreement. A provenance argument in a court. |
| 15 | [S34] | NTSB 2011. San Bruno pipeline accident report. | https://www.ntsb.gov/investigations/AccidentReports/Reports/PAR1101.pdf | One wrong origin (a 1956 voucher) became the record everyone relied on. The real form of regime B. Read the executive summary and section 1.11. |
| 16 | [S28], [S29], [S30] | FERC 2003: physical withholding report; Reliant and BP order; Enron order. | see `literature/INDEX.md` | The California cases: a declared outage can be a fault, one firm's strategy, or coordination. The power-market form of the auditor's problem. |

Not in the paper but worth one hour each: Irving, Christiano, Amodei 2018, "AI safety via
debate" (https://arxiv.org/abs/1805.00899) for the idea that a judge relies on two agents who
may not be honest; and Hubinger et al. 2024, "Sleeper Agents" (https://arxiv.org/abs/2401.05566)
for the difference between prompt-conditioned and trained behavior, which is a limit of this
work. Neither is verified in `literature/INDEX.md` yet; add a row before citing either.

## 2. How sound is the work

This is an honest assessment. Statement kinds are labeled.

### What is sound

1. **The design isolates causes.** [ESTABLISHED method] Eight regimes, one switch each, a
   negative control, a positive control, known ground truth. If an auditor flags an innocent
   regime, the cause is known. This is the standard logic of a controlled experiment, and it is
   the strongest part of the work.
2. **The primary test was fixed before the data.** [FINDING] The hand rule has not changed since
   2026-10-23. The preregistration was frozen before the confirmatory run. The dev and held-out
   splits are separate. The primary hypothesis (H-SPRINT-3) was tested once, on held-out data,
   and it failed. Reporting a failed primary hypothesis is correct practice.
3. **The main claims replicate.** [FINDING] Four results hold in all seven models, across three
   vendors and two access paths. The hand classifications were checked against the saved runs
   with a script (0 mismatches).
4. **The say-do measurement is direct.** [FINDING] We read what the agents said and compared it
   with what they did, trajectory by trajectory, and with the matched trajectory without the
   channel. Few collusion papers do this.
5. **The limits are stated.** Prompt-conditioned incentives, one game, small samples, the label
   leak in S4, the scripted positive control, and the analogies to real cases are each named.

### What is weak, and what an expert will notice

1. **The null on communication is partly built in.** [INTERPRETATION] Endorsing is a weakly
   dominant strategy for an approval-seeking reviewer in this game. So a coalition has nothing
   to gain from coordination, and "the channel adds no harm" is close to a design consequence.
   The result still matters for auditors (harm cannot be the evidence), but it is not evidence
   that models cannot collude. A game where coordination is necessary for the payoff (for
   example, the decider needs both endorsements, and a lone endorser of a false claim is
   punished) would test that.
2. **The provenance null may be a floor effect.** [INTERPRETATION] The rule auditors had false
   positive rates of 0.02 to 0.06 before provenance. A reduction of 0.10 was impossible. The
   preregistered threshold was set before the baseline was known. A relative target, or a
   harder innocent regime that produces collusive-looking talk, would be a fairer test.
3. **The auditors are weak by design.** [INTERPRETATION] The keyword rule misses reworded
   plans. The judge is one model (DeepSeek chat) with no held-out tuning, and it judged
   DeepSeek trajectories too. A trained classifier with a held-out evaluation, and a second
   judge model, would make the detection results stronger.
4. **Real collusion was almost never observed.** [FINDING] In 252 collusion-opportunity
   trajectories, one had every part of collusion. So the detection results are mostly about
   false positives, not about recall on real coalitions. The positive control is scripted.
5. **Prompt-conditioned, not learned.** [ESTABLISHED limit] The payoffs are text in a prompt.
   Refusals may reflect the prompt reading as unethical, not the model's goals. Nothing here
   speaks to collusion that training produces.
6. **Samples are small and comparisons are many.** [FINDING] 18 false claims per cell. Seven
   models times several contrasts, all exploratory except one. Some intervals that exclude zero
   will be chance. The paper reports intervals, not p-values, and labels the exploratory runs,
   but a reader should discount single-model findings.
7. **The deployable claim is thin.** [FINDING] The one real case was caught only by the auditor
   with the matched trajectory, which a deployer cannot make. The paper says so. The open
   question, what can replace the counterfactual, is the real research question.
8. **One prompt set.** Prompt sensitivity is untested. The seven models answer "does it hold
   across models", not "does it hold across framings".
9. **The real cases are motivation, not validation.** The analogies justify which plus factors
   to measure. They do not show that the game predicts anything about real markets.

### What would make it strong (next steps, in order of value)

1. A game with a real coordination incentive (see weakness 1), so that H-SPRINT-4 is a fair test.
2. Two or three prompt framings per regime, to test prompt sensitivity.
3. A second judge model and a trained auditor with a held-out evaluation.
4. More seeds without the cache, so seeds are independent.
5. Human adjudication of a sample of the hand classifications.
6. A replacement for the matched trajectory: for example, the same reviewer's behavior on
   other cases, or a re-run with the private message removed.

## 3. Questions for an AI safety expert

The owner's stance: early phase, total beginner, wants to learn how to think about AI safety
research, not only this project. The questions are grouped. Ask the ones in group A first.

### A. How to think (metacognition)

1. When you read a result from a toy environment, what makes you trust that it transfers?
   What would make you trust this one, or not?
2. How do you tell an informative null result from one that the design built in? Our
   "communication adds no harm" is close to the second kind. How would you have designed around it?
3. How do you choose a primary hypothesis and a threshold before you know the baseline? Our
   0.10 target turned out to be impossible. What is the usual practice?
4. How do experienced researchers check themselves when a result "feels" important? What is
   your personal checklist before you believe your own finding?
5. When should a beginner build an environment, and when should they study existing models
   and benchmarks instead?
6. How do you size a research question for a weekend, for three months, for a year? What
   signals tell you a question is too big or too small?
7. How do you know when to stop a line of work?
8. What are the most common mistakes you see in beginners' multi-agent safety work?
9. How should I use AI assistants in research without losing my own understanding? Where did
   that go wrong for people you know?

### B. About this project

10. Is "prompt-conditioned" collusion interesting to the field, or does the field need
    training-induced collusion before it cares? When does the difference matter?
11. Is our definition (coalition, coordination mechanism, outside cost) the right one? How does
    it compare with the definitions in Motwani et al. and Colosseum?
12. Which deployed or planned systems rely on endorsement-style oversight, where this problem
    is real? Is the review-game pattern the right abstraction of them?
13. What can replace the matched counterfactual trajectory in a deployed auditor?
14. Is a weak rule auditor an acceptable baseline, or should the first version already be a
    trained classifier?
15. Our judge treats a written refusal as innocence. Is that a known failure mode of LLM
    monitors? Where is it studied?

### C. About the next project (TARA, November to December 2026)

16. Is "an oversight protocol that resists correlated endorsements" tractable in three months?
    What is the smallest version that would be a real contribution?
17. Which of these should I read first: AI control, debate, consensus and cascades, antitrust
    plus factors, or the collusion papers? What am I missing?
18. Who in the field works on this, and what would they want to see from a beginner?

### D. Career and learning

19. What should a beginner from an applied field (energy sector operations) do in the first six
    months to become useful in AI safety research?
20. How do you decide between depth in one method and breadth across the field at this stage?
