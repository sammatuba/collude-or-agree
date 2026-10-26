"""epistemic_lab: a small, fully controlled environment for studying when agreement among
AI agents is evidence and when it is not.

Modules map to glossary terms (GLOSSARY.md at the repository root):

- bayes:     likelihood ratios, conditional independence, double counting
- cases:     case families, evidence items, origins, derivatives, provenance
- regimes:   the eight regimes as factor settings
- agents:    scripted proposer, reviewer, decider; LLM agents
- game:      one trajectory = one run of one case under one regime
- auditors:  information slices, epistemic plus-factor features, rule and LLM auditors
- metrics:   false approval rate, flag rates, AUROC, bootstrap by case family, Δ_comm
- llm:       the only module that touches the network (OpenAI-compatible, cached)
- run:       command-line entry points
"""
__version__ = "0.1.0"
