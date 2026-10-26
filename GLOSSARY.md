# Glossary: controlled vocabulary

**Rule:** one term, one concept. Every document in this repository uses the terms below
exactly as written. The "Do not write" column lists synonyms that are banned, because a
second word for the same thing makes a beginner think there are two things.

Definitions follow the sources named in `literature/INDEX.md`. Where a term is our own
working label, the entry says **(ours)**. Terms marked **(ours)** are not claims that the
literature uses them.

---

## 1. Roles

| Term | Definition | Do not write |
|---|---|---|
| **agent** | Any actor in an experiment that receives information and emits messages or actions. Can be a language model, a scripted rule, or a human. | participant, player, bot |
| **proposer** | The agent that drafts a claim and selects the evidence items shown in support of it. | author, submitter |
| **reviewer** | An agent that reads a claim and evidence and emits an endorsement, a rejection, or an abstention. | checker, validator, verifier |
| **decider** | The agent that sees the claim, evidence, and endorsements and emits the final action: approve, defer, or reject. | judge, decision agent, approver |
| **auditor** | A procedure that inspects a *completed* trajectory and outputs a verdict about whether collusion occurred. An auditor acts after the fact and does not change the trajectory. | detector, monitor, classifier (reserve "monitor" for AI control) |
| **trusted monitor** | In AI control, a less capable but trusted model or rule that watches an untrusted agent *during* execution and can block or flag actions. Source: Greenblatt et al. 2024 [R11]. | auditor, overseer |
| **untrusted agent** | In AI control, an agent assumed to possibly pursue hidden objectives against the protocol. Source: [R11]. | adversary, attacker (unless the threat model names an attacker) |
| **coalition** | A set of two or more agents that share an objective and act jointly to pursue it. | team, cartel, alliance |

## 2. Evidence and provenance

| Term | Definition | Do not write |
|---|---|---|
| **claim** | A proposition whose truth is in question, stated so that it is true or false in the world of the case. Example: "Unit 7 is commercially available at 18:00." | statement, assertion, fact |
| **ground truth** | The true value of a claim fixed by the case author before any agent sees the case. | label (reserve "label" for regime labels), answer |
| **evidence item** | One unit of evidence shown to an agent: a report, a log line, a measurement, a quote. | document, snippet, fragment, article, source (see "origin") |
| **origin** | The first observation or record from which an evidence item descends. Two evidence items with the same origin carry the same information about the claim. | source, root, primary |
| **derivative** | An evidence item produced by copying, paraphrasing, or summarizing another evidence item. A derivative adds no information about the claim beyond its origin. | copy, paraphrase, repost |
| **provenance** | The recorded chain from an evidence item back to its origin, including every derivative step. | lineage, history, citation chain |
| **evidence independence** | Two evidence items are independent when, given the claim's truth value, knowing one does not change the probability of the other. Formal statement in `foundations/01-evidence-independence.md`. | diversity, uniqueness |
| **dependence** | The failure of evidence independence. Common cause: shared origin. | correlation (reserve for measured statistics) |
| **double counting** | Treating two dependent evidence items as if they were independent, so the posterior moves more than the evidence justifies. | over-weighting, inflation |

## 3. Agreement and its explanations

| Term | Definition | Do not write |
|---|---|---|
| **agreement** | Two or more agents emit the same endorsement or the same action on the same claim. Agreement is an observation. It has no built-in cause. | consensus (reserve for the DeGroot/debate sense), convergence |
| **endorsement** | A reviewer's output that supports approval of a claim. | vote, approval (reserve "approval" for the decider) |
| **approval** | The decider's action that accepts the claim and triggers its consequence. | acceptance, sign-off |
| **invalid approval** | An approval of a claim whose ground truth is false, or whose evidence does not meet the stated approval criterion. | bad approval, false positive (reserve for auditor metrics) |
| **correlated error** | Agents make the same mistake because they share data, models, or context, with no coordination. | shared mistake, systematic error |
| **shared-source error** | A correlated error caused by evidence items that trace to one origin. One kind of correlated error. | echo chamber |
| **conformity** | A later agent changes its output toward an earlier agent's visible output, despite holding evidence that points elsewhere. | herding, peer pressure, sycophancy (sycophancy is toward the *user*, not toward peers) |
| **information cascade** | A sequence in which agents rationally imitate earlier public actions and stop using their private evidence. Source: Bikhchandani et al. 1992 [R6]. Conformity is the per-agent step; a cascade is the group pattern. | bandwagon |
| **exposure order** | The record of which agent saw which other agent's output before emitting its own. Needed to test conformity. | ordering, sequence |
| **strategic persuasion** | A sender selects messages to move a receiver toward the sender's preferred action. Formal models: Crawford and Sobel 1982 [R7], Kamenica and Gentzkow 2011 [R8]. | manipulation (too broad), influence |
| **selective disclosure** | A form of strategic persuasion that reveals only the true evidence items that favor the sender's preferred action. | cherry-picking, spin |
| **truthful-fragment manipulation** | Coordinated release of individually true evidence items that together induce a false conclusion. Source: Hu et al. 2026 [R14]. | lying with truths (paper title, not a term), montage |

## 4. Incentives, coordination, and collusion

| Term | Definition | Do not write |
|---|---|---|
| **payoff** | The numeric reward an agent receives at the end of a trajectory, as defined by the experiment. | utility (reserve for the formal game), reward (reserve for RL) |
| **accuracy-aligned objective** | A payoff that rewards the agent only for outcomes that match ground truth. | honest objective, good incentive |
| **approval-seeking objective** | A payoff that rewards the agent when the decider approves, regardless of ground truth. | misaligned objective, bad incentive |
| **incentive alignment** | Two agents are incentive-aligned when the same outcome raises both payoffs. Alignment is a property of payoffs, not of behavior. | shared interest, common goal |
| **communication channel** | A path through which one agent's message reaches another agent. Channels are public (the decider sees them) or private (the decider does not). | side channel (reserve for non-text carriers), backchannel |
| **coordination** | Two or more agents adjust their actions to one another in pursuit of a joint outcome. Coordination requires a mechanism: a channel, a shared signal, or repeated-game learning. | cooperation (too broad), alignment |
| **collusion** | Coordination among a coalition that pursues a joint objective at the expense of an outside party or the oversight process. Collusion = coalition + coordination mechanism + outside cost. All three are needed. | cheating, conspiracy, collaboration |
| **explicit collusion** | Collusion in which the coordination mechanism is a message that proposes or confirms a joint plan. | overt collusion, communicated collusion |
| **tacit collusion** | Collusive outcomes sustained by repeated-game incentives without any explicit agreement. Source: Calvano et al. 2020 [R9]. | implicit collusion, silent collusion |
| **secret collusion** | Collusion whose coordination mechanism is hidden from the monitor, for example by steganography. Source: Motwani et al. 2024 [R12]. | covert collusion, hidden collusion |
| **parallel conduct** | Agents take the same action without any coordination mechanism, usually because they face the same incentives. In antitrust law, parallel conduct alone is not illegal. Source: sprint Track 2.3 guide; Berger et al. 2025. | tacit collusion (different: tacit collusion is sustained by strategy), coincidence |
| **plus factor** | A piece of evidence that is more probable under collusion than under parallel conduct, used to upgrade a finding from "agreement" to "collusion." Borrowed from US antitrust practice. | indicator, signal (too generic), red flag |
| **epistemic plus factor (ours)** | A plus factor computed from provenance, exposure order, payoffs, channel use, or action-versus-evidence inconsistency in an agent trajectory. Our proposed contribution. | feature (reserve for the code), heuristic |
| **talk without action** | A trajectory in which messages propose coordination but no agent's action differs from its no-communication baseline. The main false-positive trap for message-based auditors. | cheap talk (reserve for the formal model), empty threat |
| **say-do inconsistency** | A measurable gap between what an agent states (in messages or stated reasons) and the action it takes. Source: sprint Track 2.2. | hypocrisy, deception (requires intent) |

## 5. Authority

| Term | Definition | Do not write |
|---|---|---|
| **epistemic authority** | The weight a claim receives because of who asserted it. Source: Hauswald 2025 [R1]. | credibility (one input to authority), trust |
| **decision authority** | The permission to change an accepted record, authorize a tool, or trigger an action. | power, access |
| **authority transition (ours)** | The step at which an endorsement (epistemic) becomes an approval (decision). Oversight failures concentrate here. | promotion, escalation |
| **semantic promotion (ours)** | Treating evidence for one claim as evidence for a stronger or different claim. Example: evidence of "testing scheduled" used to approve "commercially available." | overreach, conflation |
| **typed claim** | A claim whose predicate is drawn from a fixed vocabulary with defined relationships, so that a validator can check which transitions between predicates are permitted. | structured claim, schema claim |
| **ontology** | The fixed vocabulary of predicates and the permitted relationships among them. An ontology defines meaning. It does not guarantee that entered facts are true. | knowledge graph (one implementation), taxonomy |

## 6. Experiments

| Term | Definition | Do not write |
|---|---|---|
| **case** | One claim with its ground truth, its evidence items, and their provenance. | scenario, task, item |
| **case family** | A set of cases built from one underlying situation. Dev and held-out splits are made by case family so paraphrases never leak. | group, cluster |
| **regime** | One experimental condition: a fixed setting of payoffs, channel, provenance, and exposure order. Regimes carry letters (A, B, ...). | condition (use only when quoting a source), treatment, arm |
| **regime label** | The regime that generated a trajectory. The auditor never sees it. It is the target for detection metrics. | ground truth (reserve for claims) |
| **trajectory** | The complete log of one run of one case under one regime: evidence shown, messages, endorsements, action, payoffs. | episode (use when quoting Colosseum), run, transcript (a transcript is the message part only) |
| **seed** | The random seed for one trajectory. Several seeds per cell give variance estimates. | replicate, trial |
| **cell** | One (case, regime) pair. | condition |
| **positive control** | A trajectory built so that collusion is certain, used to prove the auditor can detect a known case. Required in the sprint report. | sanity check, smoke test |
| **negative control** | A trajectory built so that collusion is impossible, used to measure the auditor's false-positive rate. | baseline (reserve for comparison methods) |
| **information slice (ours)** | The subset of a trajectory that one auditor may see: messages only, actions only, messages and actions, or messages, actions, and provenance. | view, access level |
| **dev split** | The half of case families used to choose auditor thresholds and decision rules. | training set |
| **held-out split** | The half of case families never touched until the decision rule is frozen. | test set, validation set |
| **freeze** | The moment after which prompts, cases, metrics, and decision rules cannot change. Recorded in `PREREGISTRATION.md` with a date. | lock, finalize |
| **preregistration** | A written statement, before the main run, of hypotheses, predictions, falsifiers, and analysis plan. | protocol, plan |
| **communication effect** | Δ_comm = P(invalid approval \| channel on) − P(invalid approval \| channel off), with payoffs and case fixed. An intervention quantity, not a correlation. | collusion effect, channel effect |
| **prompt-conditioned behavior** | Behavior that follows from role instructions in a prompt. Not evidence of a learned objective or an equilibrium strategy. | emergent behavior, learned collusion |

## 7. Measurement

| Term | Definition | Do not write |
|---|---|---|
| **precision** | Among trajectories the auditor flags as collusion, the fraction whose regime label is a collusion regime. | positive predictive value |
| **recall** | Among trajectories whose regime label is a collusion regime, the fraction the auditor flags. | sensitivity, hit rate |
| **false-positive rate** | Among trajectories whose regime label is a non-collusion regime, the fraction the auditor flags. Reported separately per non-collusion regime. | false alarm rate |
| **AUROC** | Area under the receiver operating characteristic curve: the probability that a random collusion trajectory receives a higher auditor score than a random non-collusion trajectory. | AUC, ROC score |
| **Brier score** | Mean squared difference between a stated probability and the 0/1 outcome. Lower is better. Only meaningful for numeric probabilities, never for prose confidence. | calibration error (one component of Brier) |
| **false approval rate** | P(approve \| claim false). The primary decision-harm metric. | error rate |
| **true approval rate** | P(approve \| claim true). The utility metric that guards against an intervention that just rejects everything. | accuracy, hit rate |
| **deferral rate** | P(defer). Reported with the operational criterion for when deferral is correct. | abstention rate |
| **bootstrap interval** | A confidence interval obtained by resampling case families with replacement. The default uncertainty report in this repository. | error bar (describe what it is), CI (expand at first use) |

## 8. Bayesian terms

| Term | Definition | Do not write |
|---|---|---|
| **prior odds** | P(H) / P(not H) before seeing evidence. | base rate (one way to set the prior) |
| **likelihood ratio** | LR(E) = P(E \| H) / P(E \| not H). How much one evidence item favors H. | Bayes factor (same number, different usage; use "likelihood ratio") |
| **posterior odds** | Prior odds multiplied by the joint likelihood ratio of all evidence. | updated odds |
| **conditional independence** | P(E1, E2 \| H) = P(E1 \| H) P(E2 \| H), and the same given not H. The condition under which likelihood ratios multiply. | independence (always say "conditional" in this repository) |

## 9. Mechanistic terms (for the TARA project)

| Term | Definition | Do not write |
|---|---|---|
| **activation** | The vector output of one layer of a transformer at one token position. | hidden state (same thing; use "activation"), embedding (reserve for the input layer) |
| **residual stream** | The running sum that each transformer layer reads from and writes to. Activations are read from it. | hidden stream |
| **linear probe** | A logistic regression trained on activations to predict a label. A probe that works shows the label is linearly readable, not that the model uses it. | classifier head, detector |
| **anti-confound check** | A test that the probe does not predict a nuisance variable (prompt template, model family, regime wording) instead of the target. | sanity check, control |

## 10. Formal game-theory terms (used in foundations/02 and 03)

| Term | Definition | Do not write |
|---|---|---|
| **state** | The variable the sender knows and the receiver does not, in a communication game. In the review game, the claim's truth value. | hidden variable, world |
| **sender / receiver** | In cheap talk and persuasion models, the agent with private information and the agent who acts on a message. Proposer and decider play these roles. | speaker / listener |
| **private signal** | An observation available to one agent only. In the review game, a reviewer's private evidence slice. | private information (acceptable in formal text), hint |
| **public action** | An action every later agent can observe before acting. In regime C, R1's endorsement as seen by R2. | visible move |
| **weight matrix** | In the DeGroot model, the row-stochastic matrix W whose entry W_ij is the weight agent i puts on agent j's opinion. | influence matrix, trust matrix |
| **common prior** | The assumption that all agents start from the same probability distribution over states. | shared belief |
| **common knowledge** | A fact every agent knows, knows that every agent knows, and so on without end. | mutual knowledge (weaker; use only when meant) |
| **equilibrium** | A profile of strategies in which no agent gains by changing its own strategy alone. | solution, steady state |
| **babbling equilibrium** | A cheap-talk equilibrium in which messages carry no information and the receiver ignores them. | uninformative equilibrium |
| **signal structure** | In Bayesian persuasion, the sender's committed mapping from states to message probabilities. | experiment (the paper's word; avoid here), disclosure policy |
| **dominant strategy** | An action that is best for an agent regardless of what others do. In the one-shot review game, endorsing is dominant for an approval-seeking reviewer. | best move, obvious play |

## 11. Protocol and validator terms (used in foundations/05 and 06)

| Term | Definition | Do not write |
|---|---|---|
| **protocol** | The fixed mapping from (evidence items, messages, endorsements) to the decider's action, including any monitors or validators in between. The object AI control evaluates. | pipeline, workflow (acceptable in prose about the game), system |
| **safety** | In AI control, the probability that the protocol avoids the harmful outcome under the worst-case untrusted policy in the threat model. Here: 1 − false approval rate under that policy. | security, robustness |
| **usefulness** | In AI control, task performance when agents are honest. Here: true approval rate. | utility (reserve for the formal game), productivity |
| **validator** | A deterministic checker at the authority transition that rejects an approval when a mechanical condition fails (too few distinct origins, a non-permitted predicate transition, a time-validity failure). | gate, guard, filter |
| **permitted transition** | A pair (p, q) of predicates such that evidence for p may support a claim with predicate q. The set of permitted transitions is part of the ontology. | allowed inference, mapping |
| **transitive closure** | The set of all predicate pairs reachable by chaining permitted transitions. | reachability (acceptable in formal text) |

## 12. Additional mechanistic terms (used in foundations/08)

| Term | Definition | Do not write |
|---|---|---|
| **last-token pooling** | Taking the activation at the final real token of a sequence as the representation of the whole sequence. | last position |
| **mean pooling** | Averaging activations over all real tokens of a sequence. | average pooling |
| **standardization** | Subtracting the dev-split mean and dividing by the dev-split standard deviation, per dimension, before fitting a probe. | normalization (ambiguous), z-scoring (acceptable in code comments) |
| **linearly readable** | A label is linearly readable from activations when a linear probe predicts it well above chance on held-out data. Says nothing about whether the model uses it. | encoded, represented (too strong) |
| **layer sweep** | Fitting one probe per layer and reporting the metric by layer. | layer scan |
| **nuisance variable** | A variable correlated with the label that the probe could read instead of the label. Regime wording and prompt template are the main ones here. | confound (reserve for the experiment-design sense), leakage |

---

## Usage note for agents

When you need a word that is not here, add it to this file **before** using it in another
document, with a definition, a source or **(ours)**, and a "Do not write" entry. Then
use it the same way everywhere.
