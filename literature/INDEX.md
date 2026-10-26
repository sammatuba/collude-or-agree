# Literature index

**How to use.** Every work this repository may cite has a row here with an id. The id series
are: `[R]` the 2026-10-20 research starter bibliography (links checked by its author on
2026-10-20); `[S]` the Apart AI Collusion Sprint reading list (fetched from the sprint page on
2026-10-23); `[T]` TARA reading, to be added; `[W]` web resources and code; `[U]` unverified
mentions that must not be cited. A dossier in `papers/` exists where the "dossier" column is
not "none"; `data/papers.jsonl` is the machine view built by `python3 tools/build-cards.py`.

**Fidelity rule.** Cite only rows with a verified URL. For the `[S]` series the sprint page
gave author surnames, year, and URL only; titles are "not yet verified" until a dossier is
written from the paper itself. Never cite a `[U]` row. Add a row before you cite a new work.

Closeness scale (our judgment, 1 to 5): 5 = must differentiate from it before claiming
novelty; 3 = supplies a model or method we reuse; 1 = background.

## R series: research starter bibliography

| Id | Citation | Status | URL | Closeness to our question | Dossier |
|---|---|---|---|---|---|
| [R1] | Hauswald, Rico. 2025. "Artificial Epistemic Authorities." *Social Epistemology* 39(6), 716-725. | peer-reviewed | https://doi.org/10.1080/02691728.2025.2449602 | 3. Defines AI epistemic authority; identification and deference problems. | stub |
| [R2] | Goldman, Alvin I. 2001. "Experts: Which Ones Should You Trust?" *Philosophy and Phenomenological Research* 63(1), 85-110. | peer-reviewed | https://doi.org/10.1111/j.1933-1592.2001.tb00093.x | 2. Layperson choice between conflicting experts. | none |
| [R3] | Lee, John D., and Katrina A. See. 2004. "Trust in Automation: Designing for Appropriate Reliance." *Human Factors* 46(1), 50-80. | peer-reviewed | https://doi.org/10.1518/hfes.46.1.50_30392 | 1. Human reliance on automation. | none |
| [R4] | DeGroot, Morris H. 1974. "Reaching a Consensus." *Journal of the American Statistical Association* 69(345), 118-121. | peer-reviewed | https://doi.org/10.1080/01621459.1974.10480137 | 2. Weighted opinion updating; convergence is not truth. | none |
| [R5] | Aumann, Robert J. 1976. "Agreeing to Disagree." *The Annals of Statistics* 4(6), 1236-1239. | peer-reviewed | https://doi.org/10.1214/aos/1176343654 | 1. Common prior and common knowledge; a limit on what agreement implies. | none |
| [R6] | Bikhchandani, Sushil; David Hirshleifer; and Ivo Welch. 1992. "A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades." *Journal of Political Economy* 100(5), 992-1026. | peer-reviewed | https://doi.org/10.1086/261849 | 3. Information cascade model behind regime C (conformity). | stub |
| [R7] | Crawford, Vincent P., and Joel Sobel. 1982. "Strategic Information Transmission." *Econometrica* 50(6), 1431-1451. | peer-reviewed | https://doi.org/10.2307/1913390 | 3. Cheap talk; incentive misalignment limits informative messages (regime D). | stub |
| [R8] | Kamenica, Emir, and Matthew Gentzkow. 2011. "Bayesian Persuasion." *American Economic Review* 101(6), 2590-2615. | peer-reviewed | https://doi.org/10.1257/aer.101.6.2590 (author PDF https://web.stanford.edu/~gentzkow/research/BayesianPersuasion.pdf) | 3. Strategic disclosure of true information (selective disclosure). | stub |
| [R9] | Calvano, Emilio; Giacomo Calzolari; Vincenzo Denicolo; and Sergio Pastorello. 2020. "Artificial Intelligence, Algorithmic Pricing, and Collusion." *American Economic Review* 110(10), 3267-3297. | peer-reviewed | https://doi.org/10.1257/aer.20190623 | 2. Tacit collusion in repeated pricing; defines the term we use. | none |
| [R10] | Irving, Geoffrey; Paul Christiano; and Dario Amodei. 2018. "AI Safety via Debate." | preprint | https://arxiv.org/abs/1805.00899 | 2. Competing agents as oversight; assumptions on the judge. | none |
| [R11] | Greenblatt, Ryan; Buck Shlegeris; Kshitij Sachan; and Fabien Roger. 2024. "AI Control: Improving Safety Despite Intentional Subversion." *ICML 2024*, PMLR 235. | peer-reviewed | https://proceedings.mlr.press/v235/greenblatt24a.html | 4. Untrusted-agent threat model and trusted monitoring; our oversight framing. | stub |
| [R12] | Motwani, Sumeet Ramesh, et al. 2024. "Secret Collusion among AI Agents: Multi-Agent Deception via Steganography." *NeurIPS 2024*. | peer-reviewed | https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html | 4. Formal threat model for secret collusion (TM-4). | stub |
| [R13] | Hammond, Lewis, et al. 2025. "Multi-Agent Risks from Advanced AI." | report / preprint | https://arxiv.org/abs/2502.14143 | 2. Taxonomy: miscoordination, conflict, collusion. | none |
| [R14] | Hu, Jinwei; Xinmiao Huang; Youcheng Sun; Yi Dong; and Xiaowei Huang. 2026. "Lying with Truths: Open-Channel Multi-Agent Collusion for Belief Manipulation via Generative Montage." *ACL 2026*. | peer-reviewed | https://aclanthology.org/2026.acl-long.270/ (arXiv https://arxiv.org/abs/2601.01685) | 5. Truthful-fragment manipulation; closest to regime D and to selective disclosure. | stub |
| [R15] | Okawa, Maya. 2026. "Emergence of Biased Consensus in Multi-Agent LLM Debates." *ICML 2026*, PMLR 306. | peer-reviewed | https://proceedings.mlr.press/v306/okawa26a.html | 4. Conformity and noise in debate; closest to regime C. | stub |
| [R16] | Chen, Yongqiang; Gang Niu; James Cheng; Bo Han; and Masashi Sugiyama. 2025 submission, revised 2026. "When and Why Does Multi-Agent Debate Fail and Does It Really Underperform?" | preprint; version and title may change | https://arxiv.org/abs/2510.20963 | 3. Incentive framing of debate protocols. | stub |
| [R17] | Rose, Aaron; Carissa Cullen; Sahar Abdelnabi; Philip Torr; Brandon Gary Kaplowitz; and Christian Schroeder de Witt. 2026. "Detecting Multi-Agent Collusion Through Multi-Agent Interpretability." | preprint, v4 revised 2026-10-12 | https://arxiv.org/abs/2604.01151 (code https://github.com/aaronrose227/narcbench) | 5. Activation-based collusion detection (NARCBench); the TARA project's nearest work. | stub |
| [R18] | Kraidia, Insaf, et al. 2026. "When Collaboration Fails: Persuasion-Driven Adversarial Influence in Multi-Agent Large Language Model Debate." *Scientific Reports* 16, article 11640. | peer-reviewed | https://www.nature.com/articles/s41598-026-42705-7 | 4. Behavioral comparator for one persuasive agent (regime D). | stub |
| [R19] | Hong, Lu, and Scott E. Page. 2004. "Groups of Diverse Problem Solvers Can Outperform Groups of High-Ability Problem Solvers." *PNAS* 101(46), 16385-16389. | peer-reviewed | https://doi.org/10.1073/pnas.0403723101 | 1. Diversity argument; check assumptions before applying to LLM committees. | none |

## S series: Apart AI Collusion Sprint reading list (fetched 2026-10-23)

For [S1] to [S26], only surnames, year, URL, and the track that listed the work are known from the sprint page. Rows [S27] to [S46] are historical and legal grounding sources added 2026-10-26 for `projects/2026-10-apart-collusion-sprint/design/historical-grounding.md`.

| Id | Citation | Status | URL | Closeness to our question | Dossier |
|---|---|---|---|---|---|
| [S1] | Nakamura, Mason, et al. 2026. "Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems." (title from the repository README citation) | preprint; README says accepted to NeurIPS 2026 Evaluations and Datasets Track | https://arxiv.org/abs/2602.15198 | 5. Collusion auditing environment; listed under Tracks 1, 2.1, 2.3, 3.1. | stub |
| [S2] | Berger et al. 2025. Title inferred from URL slug, verify: "Coordination Code: Rethinking Antitrust Liability in the Age of AI Pricing." *ABA Antitrust Law* magazine, Fall 2025. | web page / magazine article | https://www.americanbar.org/groups/antitrust_law/resources/magazine/2025-fall/coordination-code-rethinking-antitrust-liability-age-ai-pricing/ | 4. The sprint's source for antitrust plus factors; listed under Track 2.3. | stub |
| [S3] | Lin et al. 2024. Title not yet verified. | preprint | https://arxiv.org/abs/2410.00031 | Listed under Track 2 and Track 3 reading; not yet read. | none |
| [S4] | Fish et al. 2024. Title not yet verified. | preprint | https://arxiv.org/abs/2404.00806 | Listed under Track 1 reading; not yet read. | none |
| [S5] | Bonjour et al. 2022. Title not yet verified. *PMLR* v180. | peer-reviewed | https://proceedings.mlr.press/v180/bonjour22a.html | Listed under Track 1 reading (question 1.4); not yet read. | none |
| [S6] | Bracale Syrnikov et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2601.11369 | Listed under Track 1 reading; not yet read. | none |
| [S7] | Shi et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2607.05132 | Listed under Track 2 reading; not yet read. | none |
| [S8] | Radev et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2605.29178 | Listed under Track 2 reading; not yet read. | none |
| [S9] | Nguyen et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2604.03968 | Listed under Track 2 reading; not yet read. | none |
| [S10] | Arike et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2601.21112 | Listed under Track 2 reading; not yet read. | none |
| [S11] | Tian 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2604.17774 | Listed under Track 3 reading; not yet read. | none |
| [S12] | Dietrich 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2606.09854 | Listed under Track 3 reading; not yet read. | none |
| [S13] | Kale et al. 2025. Title not yet verified. | preprint | https://arxiv.org/abs/2508.19461 | Listed under Track 3 reading; not yet read. | none |
| [S14] | Najt et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2605.16626 | Listed under Track 3 reading; not yet read. | none |
| [S15] | Jiralerspong et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2603.16928 | Listed under Track 3 reading; not yet read. | none |
| [S16] | Keppo et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2603.20281 | Listed under Track 1 reading; not yet read. | none |
| [S17] | Eschenbaum et al. 2022. Title not yet verified. | OpenReview PDF | https://openreview.net/pdf?id=BztUFukcBry | Listed under Track 1 reading; not yet read. | none |
| [S18] | Aharon et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2601.22184 | Listed under Track 1 reading; not yet read. | none |
| [S19] | Rippin et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2606.28425 | Listed under Track 1 reading; not yet read. | none |
| [S20] | Xu et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2607.26385 | Listed under Track 1 reading; not yet read. | none |
| [S21] | Collina et al. 2025. Title not yet verified. | preprint | https://arxiv.org/abs/2511.21935 | Listed under Track 1 reading; not yet read. | none |
| [S22] | Agrawal et al. 2025. Title not yet verified. | preprint | https://arxiv.org/abs/2507.01413 | Listed under Track 1 reading; not yet read. | none |
| [S23] | Q. Liu et al. 2026. Title not yet verified. | preprint | https://arxiv.org/abs/2604.23511 | Listed under Track 1 reading; not yet read. | none |
| [S24] | Tomašev et al. 2026. Title not yet verified. Sprint page labels it a "contrasting view." | preprint (PDF link) | https://arxiv.org/pdf/2512.16856 | Listed under Track 1 reading; not yet read. | none |
| [S25] | Dhanda 2026. Title not yet verified. | preprint (Research Square) | https://doi.org/10.21203/rs.3.rs-10183486/v1 | Listed under Track 1 reading; not yet read. | none |
| [S26] | Author unknown. 2026. Sprint page label: "Voluntary collusion / secret alliances." Title not yet verified. | preprint | https://arxiv.org/abs/2605.27593 | Listed under Track 3 reading; not yet read. | none |
| [S27] | FERC. 2003-03-26. "Findings at a Glance." Summary sheet for the staff "Final Report on Price Manipulation in Western Markets," Docket PA02-2-000. | verified 2026-10-26; regulator summary sheet (the full report itself not yet fetched) | https://ferc.gov/sites/default/files/2020-04/summary-findings.pdf | 2. Economic withholding in California 2000-2001; false availability (F01); grounding only. | none |
| [S28] | FERC staff. 2003-08-01. "Staff's Initial Report on Physical Withholding by Generators Selling into the California Market and Notification to Companies." | verified 2026-10-26; regulator staff report | https://ferc.gov/sites/default/files/2020-05/WithholdingReport8-1-03.pdf | 2. How an investigator separated innocent outages from withholding (sworn data requests). | none |
| [S29] | FERC. 2003-03-26. Order to show cause, Reliant and BP Energy, Dockets EL03-59 and EL03-60. 68 Fed. Reg. 15716 (2003-04-01). | verified 2026-10-26; regulator order (allegations, not final findings) | https://www.govinfo.gov/content/pkg/FR-2003-04-01/pdf/03-7797.pdf | 2. Alleged coordination through recorded trader calls; regime E1 analogue. | none |
| [S30] | FERC. 2003-06-25. Order to show cause, Enron and Partnership Entities, Docket EL03-180-000 et al. 68 Fed. Reg. 39921 (2003-07-03). Quotes the CAISO tariff list of anomalous behavior, including "unexplained or unusual redeclarations of availability by Generators". | verified 2026-10-26; regulator order (allegations, not final findings) | https://www.govinfo.gov/content/pkg/FR-2003-07-03/pdf/03-16822.pdf | 2. Alleged coordination "in concert"; tariff indicators of false availability (F01). | none |
| [S31] | FERC. 2005-12-27. "The Commission's Response to the California Electricity Crisis and Timeline for Distribution of Refunds." Report to Congress. | verified 2026-10-26; regulator report | https://www.ferc.gov/sites/default/files/2020-05/comm-response.pdf | 1. Settlement list (Williams and AES Southland, Reliant, Duke). | none |
| [S32] | The AES Corporation. 2002. Form 10-K for fiscal year 2001, Item 3 (Legal Proceedings). | verified 2026-10-26; company filing (the firm's own disclosure, not a regulator finding) | https://www.sec.gov/Archives/edgar/data/874761/000091205702011424/a2074070z10-k.htm | 1. FERC investigation of outage practices at AES plants and their marketing partner. | none |
| [S33] | FERC, NERC and Regional Entity Staff. November 2021. "The February 2021 Cold Weather Outages in Texas and the South Central United States." | verified 2026-10-26; regulator staff report | https://nerc.com/pa/rrm/ea/Documents/February_2021_Cold_Weather_Report.pdf | 2. Correlated failure from one cause; unchecked readiness declarations (attestation families). | none |
| [S34] | National Transportation Safety Board. 2011-08-30. "Pacific Gas and Electric Company Natural Gas Transmission Pipeline Rupture and Fire, San Bruno, California, September 9, 2010." Pipeline Accident Report NTSB/PAR-11/01. | verified 2026-10-26; official accident investigation report | https://www.ntsb.gov/investigations/AccidentReports/Reports/PAR1101.pdf | 3. A wrong record derived from one erroneous origin; regime B and provenance grounding. | none |
| [S35] | US Attorney's Office, Northern District of California. 2016-08-09. "PG&E Found Guilty Of Obstruction Of An Agency Proceeding And Multiple Violations Of The Natural Gas Pipeline Safety Act." Press release. | verified 2026-10-26; government press release (read through a Wayback Machine capture) | https://www.justice.gov/usao-ndca/pr/pge-found-guilty-obstruction-agency-proceeding-and-multiple-violations-natural-gas | 2. Single firm kept records it knew were inaccurate; regime D analogue. | none |
| [S36] | US Attorney's Office, Northern District of California. 2017-01-26. "PG&E Ordered To Develop Compliance And Ethics Program As Part Of Its Sentence For Engaging In Criminal Conduct." Press release. | verified 2026-10-26; government press release (read through a Wayback Machine capture) | https://www.justice.gov/usao-ndca/pr/pge-ordered-develop-compliance-and-ethics-program-part-its-sentence-engaging-criminal | 1. Sentence for [S35]. | none |
| [S37] | Supreme Court of the Philippines, En Banc. 2021-08-03. *Bayan Muna Representatives Colmenares and Zarate et al. v. Energy Regulatory Commission and Manila Electric Company (MERALCO)*, G.R. Nos. 210245, 210255, 210502. Lopez, J. | verified 2026-10-26; court decision (also at https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/1/68036) | https://lawphil.net/judjuris/juri2021/aug2021/gr_210245_2021.html | 3. ERC voided WESM prices on an unfinished investigation; the Court nullified the order; no collusion finding. | none |
| [S38] | Supreme Court of the Philippines, Third Division. 2025-11-10. *Philippine Electricity Market Corporation v. Therma Mobile, Inc.*, G.R. No. 224341. Singh, J. | verified 2026-10-26; court decision, read from an unofficial online copy (official text not yet fetched) | https://dev.lawyerly.ph/juris/70326 | 2. Single-firm Must-Offer Rule breach finding, remanded; not collusion. | none |
| [S39] | Pormon, M. M. M. (UP Visayas Tacloban College). 2017. "'Alleged Collusion' Effects in Power Supply Shortage in the Philippines." Conference paper, KEA 2017 conference (kea.ne.kr). | verified 2026-10-26; conference paper, not peer-reviewed | https://kea.ne.kr/conference-2017/download/S3-8-2_Miah%20Pormon.pdf | 1. Dates, affected plants, and WESM price levels for November and December 2013; does not test for collusion. | none |
| [S40] | *Bell Atlantic Corp. v. Twombly*, 550 U.S. 544 (2007). US Supreme Court. | verified 2026-10-26; court opinion | https://www.law.cornell.edu/supct/html/05-1126.ZO.html | 4. Parallel conduct alone does not show agreement; regime E0 and plus factors (with [S2]). | none |
| [S41] | *Interstate Circuit, Inc. v. United States*, 306 U.S. 208 (1939). US Supreme Court, decided 1939-02-13. | verified 2026-10-26; court opinion | https://www.law.cornell.edu/supremecourt/text/306/208 | 4. Agreement inferred from one invitation known to reach all, plus uniform action; regime E1. | none |
| [S42] | Court of Justice of the European Union (Fifth Chamber). 2016-01-21. *Eturas and Others*, Case C-74/14. | verified 2026-10-26; court judgment (CELEX 62014CJ0074; judgment text read from the Publications Office Cellar copy at http://publications.europa.eu/resource/celex/62014CJ0074; the EUR-Lex URL is the human-readable page) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62014CJ0074 | 5. Presumed participation from awareness of a message; rebuttal by public distancing or contrary action; regime F and reviewer refusal. | none |
| [S43] | US Department of Justice. 2015-04-06. Press release on the felony charge against David Topkins (*United States v. Topkins*, N.D. Cal.). Exact title not yet verified; the URL slug reads "former-e-commerce-executive-charged-price-fixing-antitrust-divisions-first-online-marketplace". | verified 2026-10-26; government press release (read through an Internet Archive capture) | https://web.archive.org/web/20170212181724/https://www.justice.gov/opa/pr/former-e-commerce-executive-charged-price-fixing-antitrust-divisions-first-online-marketplace | 3. Algorithm used to carry out an admitted human agreement; regime P analogue. | none |
| [S44] | US Department of Justice, Antitrust Division. Case page, *United States and Plaintiff States v. RealPage, Inc.*, No. 1:24-cv-00710 (M.D.N.C.). Page updated 2026-09-04. | verified 2026-10-26; government case docket page (allegations; no final judgment against RealPage as of the page date) | https://www.justice.gov/atr/case/us-and-plaintiff-states-v-realpage-inc | 3. Shared vendor with alleged pooled private data; status of the case. | none |
| [S45] | US Department of Justice. 2025-11-24. Press release on the proposed final judgment with RealPage. Exact title not yet verified; the URL slug reads "justice-department-requires-realpage-end-sharing-competitively-sensitive-information-and". | verified 2026-10-26; government press release (proposed settlement, not a court finding; quotes taken through a summarizer, recheck wording before quoting in the paper) | https://www.justice.gov/opa/pr/justice-department-requires-realpage-end-sharing-competitively-sensitive-information-and | 3. What the alleged mechanism was and what the settlement forbids. | none |
| [S46] | *Gibson v. Cendyn Group, LLC*, No. 24-3576 (9th Cir. 2025-08-15). Opinion by Judge Bea. | verified 2026-10-26; court opinion (affirmed dismissal on the pleadings) | https://cdn.ca9.uscourts.gov/datastore/opinions/2025/08/15/24-3576.pdf | 4. Same vendor without pooled data is not enough for an agreement claim; footnote names hub-and-spoke; provenance motivation. | none |

Also named on the sprint page without links (do not cite until a URL is verified): Zeng et al. 2026, Tao et al. 2026, Greenblatt et al. 2023.

## T series: TARA reading

TARA reading, to be added. Assign [T1].. when the curriculum reading for the project phase is known.

## W series: web resources and code

| Id | Resource | Status | URL | Use | Dossier |
|---|---|---|---|---|---|
| [W1] | Poseidon Research. 2026. `collusion_hackathon` starter repository (ten bundled codebases, `literature/` reading list, `util/poseidon_compute`). | web page / code | https://github.com/poseidon-research/collusion_hackathon | Sprint starter code; we reference, we do not import (D-003). | none |
| [W2] | UMass AI Safety. 2026. `colosseum` repository (Terrarium-based; Hospital, JiraTicket, Mass policy tasks). | web page / code | https://github.com/umass-ai-safety/colosseum | Environment behind [S1]; comparison point for our review game. | none |
| [W3] | Apart Research. 2026. AI Collusion Research Sprint page (tracks, rules, budget, reading list). | web page, fetched 2026-10-23 | https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 | Sprint rules and reading-list source. | none |

## U series: unverified mentions (do not cite)

| Id | Mention | Status |
|---|---|---|
| [U1] | "Liao 2026, Auditing Provenance Sensitivity" | UNVERIFIED: mentioned in a chat transcript, no URL checked; do not cite. |
| [U2] | "Kovacic et al., plus factors, Michigan Law Review" | UNVERIFIED: mentioned in a chat transcript, no URL checked; do not cite. Use [S2] for plus factors until verified. |
