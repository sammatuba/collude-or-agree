---
title: "Historical grounding: real oversight cases behind the review game"
status: draft
updated: 2026-10-26
depends_on: [GLOSSARY.md, design/regimes.md]
---

# Historical grounding: real oversight cases behind the review game

**Terms:** proposer, reviewer, decider, auditor, claim, ground truth, evidence item, origin,
derivative, provenance, agreement, correlated error, shared-source error, conformity,
strategic persuasion, selective disclosure, parallel conduct, plus factor, coordination,
coalition, collusion, explicit collusion, talk without action, communication channel,
payoff, regime, case family. All from `GLOSSARY.md`.

**Source rule.** Every event below has an `[S]` id from `literature/INDEX.md`. All rows
were fetched and checked on 2026-10-26. A detail that we could not read in a fetched
primary text is marked "not yet verified" or is left out. Section 7 lists what we could not
verify.

**Terms from law and regulation.** Some sections use words from court opinions and
regulator reports. These words are not in `GLOSSARY.md`. Each one appears in quotation
marks, with its source id, and with the glossary term it maps to. We do not use these words
without quotation marks.

## 1. Purpose

The sprint cases are fictional claims about a power utility. Examples: "Unit 7 at Ilog Plant
is commercially available at 18:00" and "the pressure sensor was calibrated." The owner
asked whether these cases are grounded in how real oversight works. This file answers with
documented events.

Each real event below shows one explanation of agreement, or one way that an oversight body
failed or succeeded. Each event also shows what an investigator needed before a court or
regulator would accept a finding of collusion.

**The limit of every analogy in this file.** Real events differ from the review game in
four ways.

1. **Real firms have real payoffs.** Our agents have payoffs that a prompt states. Their
   behavior is prompt-conditioned. A real firm's behavior is not.
2. **Real investigators have more power.** FERC (the US Federal Energy Regulatory Commission)
   sent data requests with sworn admissions. Courts heard witnesses. Our auditor reads one
   finished trajectory and nothing else.
3. **Real records are long and messy.** One trajectory has five evidence items. A real
   investigation reads years of records.
4. **Legal standards are not detection metrics.** A court asks whether evidence meets a
   standard of proof. Our auditor outputs a score. A legal standard can guide which plus
   factors we measure. It cannot tell us a threshold.

Every mapping from a real event to a regime is an [INTERPRETATION]. No event below is
evidence about language-model agents.

## 2. The core mapping

[INTERPRETATION] This table maps each game element to its closest counterpart in electricity
market oversight. The right column names the real case that shows the counterpart.

| Game element | Real-world counterpart | Shown in |
|---|---|---|
| **Claim** | An operational attestation: a unit's declared availability, an offer of capacity, a pipeline record, a winter-readiness declaration. | S30, S33, S34 |
| **Proposer** | The firm that makes the attestation: a generator owner, a pipeline operator, a trader. | S29, S34 |
| **Reviewer** | A second party whose action supports the attestation. Examples: a contractual partner that markets the unit's power, a counterparty trader, a competitor whose offer behavior looks the same. No real case has a clean counterpart. | S29, S32 |
| **Decider** | The body that relies on the attestation and acts: the system operator that dispatches units and sets prices, or the regulator that approves rates. | S33, S37 |
| **Auditor** | The investigator that reads the records after the outcome: FERC staff, the NTSB (US National Transportation Safety Board), the PEMC (Philippine Electricity Market Corporation) enforcement office, a court. | S28, S34, S38 |
| **Evidence item** | One record: an outage report, a redeclaration of availability, an offer, a database entry, a recorded phone call. | S30, S34, S29 |
| **Origin** | The first record of the physical state. Example: a 1956 accounting voucher was the origin of a pipeline database entry. | S34 |
| **Derivative** | A record copied from an earlier record. Example: the database entry copied the voucher's wrong pipe description. | S34 |
| **Private communication channel** | A path the decider does not see. Examples: trader phone calls, a contract between a plant and its power marketer, a platform message to its users, a letter to competitors. | S29, S32, S42, S41 |
| **Payoff** | Spot-market revenue for the proposer; refunds, penalties, or prison for the coalition if an investigator finds the conduct. | S31, S36, S43 |

**Why the reviewer row is weak [INTERPRETATION].** Real markets rarely have two named
endorsers who each endorse one attestation. The nearest counterparts are a partner firm and a
competitor that takes the same action. The paper should say so. It should not claim that
real oversight has the exact structure of the review game.

## 3. Verified events and cases

### 3.1 California electricity crisis, 2000 to 2001: false availability and coordination by trading

**What happened.**

- [FINDING] FERC staff released its "Final Report on Price Manipulation in Western Markets"
  on 2003-03-26 (Docket PA02-2-000). FERC's summary sheet states: "Electricity prices in
  California's spot markets were affected by economic withholding and inflated price
  bidding, in violation of tariff anti-gaming provisions" [S27].
- [FINDING] The same summary states: "Without underlying market dysfunction, attempts to
  manipulate the market would not be successful" [S27].
- [FINDING] The tariff of the California system operator (CAISO) listed evidence of
  anomalous behavior. The list included "withholding of Generation capacity under
  circumstances in which it would normally be offered" and "unexplained or unusual
  redeclarations of availability by Generators" [S30].
- [FINDING] On 2003-08-01 FERC staff reported on "physical withholding" (the report's term:
  keeping a generating unit out of the market). Staff studied 2000-05-01 to 2001-06-30.
  Staff sent data requests, with "an admission or denial, under oath", to "approximately 100"
  entities [S28].
- [FINDING] For one firm, Duke, staff wrote that the reasons for its outages "have been
  adequately explained." For the entities in that report, staff found "no credible evidence,
  at this time, to support further investigation" [S28].
- [FINDING] In December 2003 FERC approved a settlement with Duke for USD 2.5 million. FERC
  states that it "resolved allegations that Duke Energy had engaged in anomalous bidding and
  improperly withheld its power supply" [S31].
- [FINDING] In April 2001 FERC "approved a settlement" in which Williams Energy Marketing &
  Trading agreed to pay USD 8 million in refunds. AES Southland was also a party [S31].
- [FINDING] AES Corporation's own annual report for 2001 states that FERC investigated "the
  maintenance and outage practices and schedules" at the AES Alamitos and AES Huntington
  Beach plants. The investigation "also focuses on" Williams, the plants' "contractual
  partner" that marketed their power [S32]. This is the firm's own disclosure, not a FERC
  finding.
- [FINDING] FERC ordered Reliant and BP Energy to show cause on 2003-03-26. The order states
  that staff evidence "indicates that Reliant and BP Energy appear to have engaged in
  coordinated efforts to manipulate electricity prices." A BP trader phoned a Reliant trader
  and asked him to "lift his offer." When staff asked for transcripts, BP Energy said it "did
  not keep telephone records" [S29].
- [FINDING] A FERC order of 2003-06-25 states there is evidence that Enron and other
  entities "worked in concert through partnerships, alliances or other arrangements" [S30].
- An order to show cause is an allegation, not a final finding. Reliant later settled for
  USD 50 million. The settlement covered "the market manipulation investigation, physical
  withholding investigation, and anomalous bidding investigation" [S31].

**Explanation of agreement it shows.** Two kinds appear. First, a single firm that withholds
a unit or redeclares availability falsely. This maps to a false claim by one proposer, as in
regime D. Second, firms that coordinate through phone calls or contracts. This maps to
explicit collusion through a private communication channel, as in regime E1.

**What the decider had to decide.** CAISO had to dispatch units and settle prices from the
availability that generators declared. It could not inspect each unit in real time.

**What made it hard.** An outage has innocent causes: a real equipment fault or planned
maintenance. Staff needed each firm's sworn explanation to separate them. The Duke record
also shows that a verdict can change: staff accepted Duke's explanation in August 2003, and
FERC settled withholding allegations with Duke in December 2003 [S28], [S31].
[INTERPRETATION] The coordination findings rested on recorded calls and contract records.
These are messages plus actions, not agreement alone.

**Limit of the analogy.** The crisis involved many firms, many strategies, and a flawed
market design [S27]. Our game has one claim and three agents. We could not read the Final
Report itself (see section 7). We cite it only through FERC's own summary and orders.

### 3.2 Philippine WESM, November and December 2013: common cause, withholding, and an unfinished investigation

WESM is the Wholesale Electricity Spot Market of the Philippines. ERC is the Energy
Regulatory Commission. PEMC is the Philippine Electricity Market Corporation.

**What happened.**

- [FINDING] The Malampaya gas facility shut down for scheduled maintenance in late 2013.
  A Supreme Court decision gives the dates as 2013-11-09 to 2013-12-08 [S38]. A conference
  paper gives 2013-11-11 to 2013-12-10 [S39]. We did not resolve this difference.
- [FINDING] The conference paper states that the shutdown "affected Ilijan, Sta. Rita and
  San Lorenzo power plants." It also lists forced outages at other plants [S39]. These three
  plants are the ones the paper links to the shutdown. [INTERPRETATION] One cause then
  removed several plants at once.
- [FINDING] The conference paper reports that average WESM prices rose "from an average of
  P13.74/kwh in October to P33.22/kwh in November and P36.09/kwh in December 2013" [S39].
  This paper is not peer-reviewed, and we did not compare these numbers with PEMC data.
- [FINDING] On 2014-03-03 the ERC issued an order in ERC Case No. 2014-021 MC. As quoted by
  the Supreme Court, the order found that "prices in WESM during the November and December
  2013 supply months could not qualify as reasonable." The order "VOIDS these Luzon WESM
  prices" and imposed regulated prices. It also directed PEMC to investigate a "possible
  breach of Must-Offer Rule" [S37].
- [FINDING] The "Must-Offer Rule" (WESM term) requires a generator to offer its available
  capacity to the market. A 2025 Supreme Court decision states that the rule "was established
  to ensure that all available capacity is visible and accessible to the market" [S38].
- [FINDING] On 2021-08-03 the Supreme Court, en banc, declared the ERC order of 2014-03-03
  "NULL and VOID." The Court noted that the order "acknowledged that it was based on an
  unfinished investigation." The ERC was still "completing its findings on the possible abuse
  of market power" [S37].
- [FINDING] The Court's majority made no finding on collusion or on withholding [S37].
- [FINDING] PEMC's enforcement office found that one generator, Therma Mobile, Inc., had
  breached the Must-Offer Rule. It assessed "PHP 234.9 million in financial penalty for 3,578
  counts of breach" [S38].
- [FINDING] On 2025-11-10 the Supreme Court (Third Division) held that PEMC's investigation
  "remains valid notwithstanding" the voided ERC order. The Court remanded the question of
  Therma Mobile's liability to the Court of Appeals [S38]. As of 2026-10-26 we found no
  final outcome. We read this decision from an unofficial online copy.

**Explanation of agreement it shows.** Many generators were unavailable at the same time.
[INTERPRETATION] Two explanations compete. The first is a common cause: the Malampaya
shutdown and coinciding maintenance. This is like correlated error and parallel conduct
(regimes B and E0). The second is coordinated withholding: collusion (regime E1). Public
allegations of collusion were made in 2013 and 2014. We do not cite them, because we could
verify them only from news reports.

**What the decider had to decide.** The ERC had to decide whether the prices were the
outcome of a competitive market. It acted before its investigation into "possible abuse of
market power" was complete [S37].

**What made it hard.** The common cause was real and public. It could explain much of the
supply loss. [INTERPRETATION] To show collusion, an investigator must also show a
coordination mechanism. The only adjudicated finding we verified is a breach by one firm,
and that finding is not final [S38]. A breach by one firm is not collusion. It needs no
coalition.

**Limit of the analogy.** The Supreme Court voided the ERC order for reasons of process,
not because it found that no withholding occurred [S37]. This case does not show that
the agreement was innocent. It shows that agreement plus a common cause was not enough for
a regulator to act on safely. The sprint case families use Philippine-style names. They do
not model WESM rules, plant names, or ERC procedure.

### 3.3 Texas Winter Storm Uri, February 2021: one cause, many failures, unchecked declarations

**What happened.**

- [FINDING] The FERC-NERC staff report (November 2021) states that cold and freezing
  precipitation "led 1,045 individual BES generating units (with a combined 192,818 MW of
  nameplate capacity)" to have "4,124 outages, derates or failures to start" [S33]. NERC is
  the North American Electric Reliability Corporation. BES is the bulk electric system.
- [FINDING] Freezing issues caused 44.2 percent and fuel issues caused 31.4 percent of these
  events. Natural gas supply issues caused 87 percent of the fuel-issue events [S33].
- [FINDING] The report states that "81 percent of the freeze-related generating unit outages
  occurred at temperatures above the unit's stated ambient design temperature" [S33].
- [FINDING] ERCOT (the Texas system operator) required each generator owner to submit an
  annual declaration that it had completed its winter preparations. "Ninety-six percent (147
  of 153)" had submitted one for winter 2020/2021 [S33].
- [FINDING] The report states: "The required declarations are not used to measure the
  generating unit's performance" [S33].
- [FINDING] The report recommends considering "the potential for correlated outages for units
  served by the same pipeline(s)" [S33].
- [FINDING] The report's scope "did not include potential market manipulation," which FERC's
  Office of Enforcement examined separately [S33]. We did not verify any outcome of that work.

**Explanation of agreement it shows.** [INTERPRETATION] Correlated error from a common
cause. Many units failed together because they shared one cause (cold) and, for some, one
gas pipeline. No coordination is needed to explain this.

**What the decider had to decide.** ERCOT relied on generators' declared readiness and
declared availability to plan the system.

**What made it hard.** Each declaration was a claim that one firm made about itself. The
oversight process collected the declarations but did not test them [S33].

**Limit of the analogy.** Uri is correlated *equipment failure*. Regime B is correlated
*evidence error*: several evidence items repeat one origin. The only part that maps is
"one cause, many identical outputs." The winter declarations map better to the attestation
case families (F05, F06, F11) than to regime B.

### 3.4 PG&E San Bruno pipeline, 2010: a wrong record copied from one origin

PG&E is Pacific Gas and Electric Company. CPUC is the California Public Utilities
Commission.

**What happened.**

- [FINDING] A PG&E gas transmission pipeline ruptured in San Bruno, California, on
  2010-09-09 [S34].
- [FINDING] PG&E's geographic information system (GIS) recorded the failed segment as
  "seamless steel pipe API 5L X42." The record came "from accounting records rather than
  engineering records": a 1956 journal voucher "which contained an erroneous material
  description" [S34].
- [FINDING] The NTSB found that the segment "was not X42 seamless pipe." It contained short
  pipe pieces that the GIS did not show, some with partly welded seams [S34].
- [FINDING] The NTSB found that PG&E's integrity management program "was based on incomplete
  and inaccurate pipeline information." It found that "PG&E did not use conservative values
  for missing and assumed data" [S34].
- [FINDING] The NTSB found that the CPUC's "ineffective enforcement posture" let PG&E's
  failures continue "over many years." It named the CPUC's failure to detect the program's
  inadequacies as a contributing cause [S34].
- [FINDING] On 2016-08-09 a federal jury found PG&E guilty of five violations of the
  Natural Gas Pipeline Safety Act and of obstructing the NTSB investigation. The US
  Attorney states that PG&E "willfully failed to address recordkeeping deficiencies"
  while "knowing that their records were inaccurate or incomplete" [S35].
- [FINDING] On 2017-01-26 the court imposed "the $3 million monetary penalty" and "the
  maximum term of five years' probation" [S36].

**Explanation of agreement it shows.** [INTERPRETATION] This is the clearest real example of
an origin and a derivative. One wrong origin (the voucher) produced a derivative (the GIS
entry). Later analyses relied on the derivative. Any check that read only the GIS would
"agree" with the voucher. This is shared-source error in the evidence sense of regime B.
The criminal case adds a second element: a single firm kept records it knew were
inaccurate. That is closer to a false claim by one proposer (regime D).

**What the decider had to decide.** PG&E's own integrity program and the CPUC had to decide
whether the pipeline was safe to operate at its pressure. Both relied on PG&E's records.

**What made it hard.** The record looked like an engineering record. Its provenance (an
accounting voucher) was not visible to people who used it. The NTSB found the error only
after the rupture, by inspecting the pipe itself [S34].

**Limit of the analogy.** The NTSB does not state that the 1956 record was falsified on
purpose. No coalition is involved. This case grounds provenance and attestation families,
not collusion.

### 3.5 Bell Atlantic Corp. v. Twombly (US Supreme Court, 2007): parallel conduct is not agreement

**What happened.** [FINDING] The Court held that a claim of illegal agreement needs "enough
factual matter (taken as true) to suggest that an agreement was made." It wrote: "Without
more, parallel conduct does not suggest conspiracy." It also restated that "'conscious
parallelism'" is "'not in itself unlawful'" [S40].

[FINDING] In footnote 4 the Court quotes a treatise. It describes suspicious conduct as
"parallel behavior that would probably not result from chance, coincidence, independent
responses to common stimuli, or mere interdependence unaided by an advance understanding
among the parties" [S40].

**Explanation of agreement it shows.** Parallel conduct (regime E0).

**What the decider had to decide.** Whether a complaint that alleged only parallel conduct
could go forward. The Court said no.

**What made it hard.** [INTERPRETATION] Parallel conduct and collusion produce the same
visible actions. Only extra evidence, the plus factors, can separate them. The term "plus
factor" appears in the opinion only in quotations from the lower court [S40]. Our glossary
takes the concept from [S2].

**Limit of the analogy.** Twombly sets a pleading standard: what a complaint must allege
before discovery. It is not a rule for weighing evidence after discovery. [INTERPRETATION]
Footnote 4 reads like a likelihood-ratio test. It is a quotation, not a holding.

### 3.6 Interstate Circuit v. United States (US Supreme Court, 1939): coordination through one letter to all

**What happened.** [FINDING] A theater company's manager sent one letter to eight film
distributors. "Each letter" named "all of them as addressees." The letter demanded a minimum
admission price and no double features [S41].

[FINDING] The Court held: "It was enough that, knowing that concerted action was
contemplated and invited, the distributors gave their adherence to the scheme and
participated in it." It added: "Each distributor was advised that the others were asked to
participate" [S41].

**Explanation of agreement it shows.** Collusion through a shared signal. The distributors
did not need to message each other. One message to all, known to reach all, plus action on
it, was the coordination mechanism.

**What the decider had to decide.** Whether an agreement could be inferred without direct
evidence of one. The Court relied on "the substantial unanimity of action taken upon" the
proposals, and on the manner in which they were made [S41].

**What made it hard.** [INTERPRETATION] There was no direct agreement among the
distributors. The plus factors were the shared letter, each recipient's knowledge that all
had received it, and the uniform action that followed.

**Limit of the analogy.** [INTERPRETATION] This maps closely to our regime E1. Our proposer
sends one private message to both reviewers, who each know the other received it. But the
distributors had a real profit motive. Our reviewers have a prompted payoff.

### 3.7 Eturas (Court of Justice of the European Union, Case C-74/14, 2016-01-21): a platform message, awareness, and how to rebut participation

**What happened.**

- [FINDING] The administrator of a shared online booking system (E-TURAS) sent travel
  agencies a message about capping online discounts at 3 percent. The system then applied
  the cap. Agencies could still give larger discounts, but they "were nevertheless required to
  take additional technical steps in order to do so" [S42], paragraph 12.
- [FINDING] A "concerted practice" (EU law term: coordination short of a formal agreement)
  "implies, in addition to the participating undertakings concerting with each other,
  subsequent conduct on the market and a relationship of cause and effect between the two"
  [S42], paragraph 42.
- [FINDING] An agency "may be presumed to have participated" if "it was aware of the content
  of that message" [S42], paragraph 44. The court may not infer awareness "from the mere
  dispatch of the message" [S42], paragraph 39.
- [FINDING] An agency can rebut the presumption "by proving that it publically distanced
  itself from that practice or reported it to the administrative authorities" [S42],
  paragraph 46. "A clear and express objection sent to the administrator" can also rebut it
  [S42], paragraph 48.
- [FINDING] The presumed link between the message and conduct "could be rebutted by evidence
  of a systematic application of a discount exceeding the cap in question" [S42],
  paragraph 49.

**Explanation of agreement it shows.** [INTERPRETATION] This is the closest real statement
of talk without action (regime F). A collusive message reached every agency. An agency whose
actions contradicted the message (discounts above the cap) could rebut the presumption. An
agency that objected ("public distancing", the court's term) could also rebut it. That is
our reviewer who refuses a proposed plan.

**What the decider had to decide.** Whether receipt of a message, plus a technical
restriction, makes each recipient a member of a coalition.

**What made it hard.** The message was one-way. Agencies did not reply. The court had to
decide what silence plus aligned conduct means.

**Limit of the analogy.** [INTERPRETATION] Eturas presumes participation once awareness is
shown. Our regime F is labeled non-collusion, because its reviewers have accuracy-aligned
payoffs. Eturas does not support that label directly. It supports the narrower point: an
auditor must check whether actions followed the message, and contrary action is evidence
against collusion.

### 3.8 United States v. Topkins (US Department of Justice, 2015): an algorithm that carries out a human agreement

**What happened.** [FINDING] On 2015-04-06 the US Department of Justice (DOJ) charged David
Topkins with a felony for "conspiring to fix the prices of posters sold online" through
Amazon Marketplace. He agreed to plead guilty and to pay a USD 20,000 criminal fine. DOJ
stated that the plea agreement was "subject to court approval" [S43].

[FINDING] DOJ states that "the defendant and his co-conspirators adopted specific pricing
algorithms for the sale of certain posters with the goal of coordinating changes to their
respective prices" [S43].

**Explanation of agreement it shows.** Explicit collusion. The algorithm was the tool that
carried out an agreement that people made first.

**What the decider had to decide.** Not applicable. This was a criminal charge with a plea.

**What made it hard.** [INTERPRETATION] Identical algorithmic prices alone would look like
parallel conduct. The agreement among the sellers made it collusion.

**Limit of the analogy.** [INTERPRETATION] The guilty plea is an admitted coordination. It is
the real counterpart of our positive control (regime P), where collusion is certain by
construction. We did not verify whether the court accepted the plea or what sentence
followed.

### 3.9 RealPage (DOJ, 2024 to 2026) and Gibson v. Cendyn (9th Circuit, 2025): a shared vendor, with and without pooled data

**What happened: RealPage. These are allegations, not court findings.** We read the DOJ
quotes in [S45] through a web summarizer. Recheck the wording before quoting it in the paper.

- [FINDING] DOJ and several states filed a complaint against RealPage, Inc. on 2024-08-23
  and an amended complaint on 2025-01-07 [S44].
- [FINDING] DOJ alleges that RealPage's software "relied on nonpublic, competitively
  sensitive information shared by landlords to set rental prices" [S45].
- [FINDING] On 2025-11-24 DOJ filed a proposed final judgment with RealPage. RealPage must
  stop having its software use competitors' nonpublic information to set prices "in runtime
  operation" [S45].
- [FINDING] As of the case page's update on 2026-09-04, the court had entered a final
  judgment for one landlord (Greystar, 2026-03-02). It had not entered one for RealPage
  itself [S44].

**What happened: Gibson v. Cendyn.**

- [FINDING] On 2025-08-15 the Ninth Circuit affirmed dismissal of a claim against hotels that
  "independently purchased licenses for the same software." The software "did not share
  confidential information among the competing licensees" [S46].
- [FINDING] The court wrote: "obtaining information from the same source does not reduce the
  incentive to compete." It added that the analysis "might change" if the vendor had shared
  each hotel's confidential information among the licensees [S46].
- [FINDING] The court also wrote that if competing hotels "could all agree to abide by those
  recommendations," that "would be a hub-and-spoke conspiracy." The plaintiffs had waived
  that claim [S46]. "Hub-and-spoke" is the court's term for coordination through a central
  party. In our game, the proposer's private message to both reviewers is the hub.

**Explanation of agreement it shows.** [INTERPRETATION] Gibson is a shared origin of advice
without coordination. This is like shared-source error and parallel conduct (regimes B and
E0). RealPage, as alleged, adds pooled private data and alignment features. That moves the
shared vendor toward a coordination mechanism (regime E1).

**What the decider had to decide.** Whether using the same vendor is, by itself, evidence of
agreement. The Ninth Circuit said no, on the facts alleged.

**What made it hard.** Both settings produce similar prices. The difference is in the data
flow, which is provenance. [INTERPRETATION] This is our provenance information slice in a
legal form.

**Limit of the analogy.** Gibson decided what a complaint alleged. It made no finding that
no data was shared. Other courts may decide such cases differently; we did not verify later
decisions. RealPage is unresolved as to RealPage itself.

## 4. Regimes and the closest real case

All entries are [INTERPRETATION].

| Regime | What it isolates | Closest verified case | One-sentence link |
|---|---|---|---|
| **A** | Legitimate corroboration (negative control) | no verified case | A control needs no real counterpart; independent evidence that agrees correctly does not produce an investigation. |
| **B** | Shared-source error | San Bruno [S34]; Uri [S33] | At San Bruno one wrong origin became the database record that later analyses relied on; at Uri one cause failed many units at once. |
| **C** | Conformity | no verified case | We found no documented oversight case in which a second reviewer copied a first reviewer's visible endorsement. |
| **D** | Single-agent strategic persuasion | PG&E conviction [S35]; Therma Mobile Must-Offer breach [S38] | One firm kept records it knew were inaccurate, or did not offer capacity it had, with no coalition shown. |
| **E0** | Parallel conduct | Twombly [S40]; Gibson v. Cendyn [S46]; WESM 2013 common cause [S37], [S39] | Same action from the same incentive or the same input is not, by itself, agreement. |
| **E1** | Explicit collusion opportunity | Interstate Circuit [S41]; Reliant and BP Energy order, an allegation [S29] | One message known to reach all, plus action on it, gave the coordination mechanism; in the FERC order, recorded calls are the alleged mechanism. |
| **F** | Talk without action | Eturas [S42] | A recipient of a collusive message can rebut participation by objecting or by acting contrary to the message. |
| **P** | Certain collusion (positive control) | Topkins [S43] | A guilty plea admits the coalition, the mechanism, and the outside cost. |

## 5. What this grounding changes

1. **Define the F01 predicate.** "Commercially available" is not a standard market term in
   the sources we read. The sources speak of declared availability, redeclarations of
   availability, and offers [S30], [S38]. Suggested wording: "Unit 7 at Ilog Plant was
   available for dispatch at 18:00, as declared by the plant to the system operator." If the
   owner keeps "commercially available," the paper should define it in one sentence.
2. **Describe the attestation families as attestations.** Families F05 (sensor calibrated),
   F06 (generator test passed), F07 (permit approved), F10 (inventory matched the ledger), and
   F11 (training completed) are each
   a record that one party makes and another party relies on. Uri shows that such
   declarations can be collected without any check of performance [S33]. San Bruno shows
   that a record can descend from a wrong origin [S34]. The paper can say this in one
   sentence per family group.
3. **Add a sentence to the introduction about regulators.** Suggested text: "Regulators face
   the same problem. In 2014 the Philippine Energy Regulatory Commission voided spot-market
   prices before its investigation was complete; in 2021 the Supreme Court nullified that
   order [S37]."
4. **Anchor regime F and reviewer refusal in Eturas.** The paper can state: "EU law lets a
   recipient of a collusive message rebut participation by objecting or by acting against
   the message [S42]. Our action-based auditors apply the same test." This gives the
   talk-without-action result a legal precedent. The paper must also state the limit in
   section 3.7.
5. **Use Interstate Circuit to describe the private message.** The proposer's private message
   to both reviewers has the structure of the 1939 letter: one invitation, known to reach
   all [S41]. This explains why an endorsement that follows the message is a plus factor.
6. **Use Gibson to motivate provenance.** Same vendor without pooled data was not enough for
   a claim; the court said pooled data "might change" the analysis [S46]. This is a real
   example of provenance separating innocent from suspicious agreement.
7. **State the limit once in the paper.** Suggested text: "Real investigators used sworn
   answers, recorded calls, and physical inspection. Our auditor reads only one trajectory.
   The analogies motivate our plus factors; they do not validate them."
8. **Do not imply that WESM 2013 was collusion.** No court we read found collusion [S37],
   [S38]. If the paper mentions it, it should present it as a case where a common cause and
   a collusion hypothesis were both open.

## 6. Sources

Full rows, with status and closeness, are in `literature/INDEX.md`.

| Id | Short citation | URL |
|---|---|---|
| [S27] | FERC 2003, "Findings at a Glance", summary sheet for the staff "Final Report on Price Manipulation in Western Markets" | https://ferc.gov/sites/default/files/2020-04/summary-findings.pdf |
| [S28] | FERC staff 2003, Initial Report on Physical Withholding | https://ferc.gov/sites/default/files/2020-05/WithholdingReport8-1-03.pdf |
| [S29] | FERC 2003, Order to show cause, Reliant and BP Energy, 68 Fed. Reg. 15716 | https://www.govinfo.gov/content/pkg/FR-2003-04-01/pdf/03-7797.pdf |
| [S30] | FERC 2003, Order to show cause, Enron partnerships, 68 Fed. Reg. 39921 | https://www.govinfo.gov/content/pkg/FR-2003-07-03/pdf/03-16822.pdf |
| [S31] | FERC 2005, Report to Congress on the California crisis | https://www.ferc.gov/sites/default/files/2020-05/comm-response.pdf |
| [S32] | AES Corporation 2002, Form 10-K for 2001 | https://www.sec.gov/Archives/edgar/data/874761/000091205702011424/a2074070z10-k.htm |
| [S33] | FERC, NERC and Regional Entity staff 2021, February 2021 Cold Weather Outages | https://nerc.com/pa/rrm/ea/Documents/February_2021_Cold_Weather_Report.pdf |
| [S34] | NTSB 2011, San Bruno Pipeline Accident Report NTSB/PAR-11/01 | https://www.ntsb.gov/investigations/AccidentReports/Reports/PAR1101.pdf |
| [S35] | US Attorney N.D. Cal. 2016, PG&E found guilty | https://www.justice.gov/usao-ndca/pr/pge-found-guilty-obstruction-agency-proceeding-and-multiple-violations-natural-gas |
| [S36] | US Attorney N.D. Cal. 2017, PG&E sentence | https://www.justice.gov/usao-ndca/pr/pge-ordered-develop-compliance-and-ethics-program-part-its-sentence-engaging-criminal |
| [S37] | Supreme Court of the Philippines 2021, Colmenares et al. v. ERC and MERALCO | https://lawphil.net/judjuris/juri2021/aug2021/gr_210245_2021.html |
| [S38] | Supreme Court of the Philippines 2025, PEMC v. Therma Mobile (unofficial copy) | https://dev.lawyerly.ph/juris/70326 |
| [S39] | Pormon 2017, conference paper on the 2013 supply shortage | https://kea.ne.kr/conference-2017/download/S3-8-2_Miah%20Pormon.pdf |
| [S40] | Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007) | https://www.law.cornell.edu/supct/html/05-1126.ZO.html |
| [S41] | Interstate Circuit, Inc. v. United States, 306 U.S. 208 (1939) | https://www.law.cornell.edu/supremecourt/text/306/208 |
| [S42] | Eturas and Others, CJEU Case C-74/14 (2016) | http://publications.europa.eu/resource/celex/62014CJ0074 |
| [S43] | DOJ 2015, Topkins charged (archived release) | https://web.archive.org/web/20170212181724/https://www.justice.gov/opa/pr/former-e-commerce-executive-charged-price-fixing-antitrust-divisions-first-online-marketplace |
| [S44] | DOJ case page, US and Plaintiff States v. RealPage | https://www.justice.gov/atr/case/us-and-plaintiff-states-v-realpage-inc |
| [S45] | DOJ 2025, proposed RealPage settlement release | https://www.justice.gov/opa/pr/justice-department-requires-realpage-end-sharing-competitively-sensitive-information-and |
| [S46] | Gibson v. Cendyn Group, No. 24-3576 (9th Cir. 2025) | https://cdn.ca9.uscourts.gov/datastore/opinions/2025/08/15/24-3576.pdf |

## 7. Not verified (do not cite until checked)

- The text of FERC's Final Report of 2003-03-26 itself. CAISO-hosted copies did not load.
  Its page numbers and its exact wording on Enron strategies are not yet verified.
- AES and Williams details: unit numbers, outage dates in 2000, revenue figures, and any
  admission language. Only the USD 8 million refund [S31] and the investigation scope [S32]
  are verified.
- The text of the ERC order of 2014-03-03. We read it only as quoted by the Supreme Court
  [S37]. Phrases such as "widespread withholding" appear only in secondary sources.
- News reports of the 2013 WESM episode. These include an ERC official's figure for capacity
  not offered, legislators' collusion allegations, and a 2017-11-07 Court of Appeals ruling
  reported to reinstate the prices. All are not yet verified from primary documents.
- Any PEMC Market Surveillance Committee report, DOE or Philippine Competition Commission
  finding on the 2013 episode.
- The outcome of FERC Office of Enforcement work on February 2021.
- Whether the court accepted Topkins's plea, and his sentence.
- Whether any later appellate decision on shared pricing software disagrees with Gibson.
- [S38] was read from an unofficial online copy. The official Supreme Court text is not yet
  fetched.
- Exact titles of the DOJ releases [S43] and [S45].
