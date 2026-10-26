# %% [markdown]
# # 01. Evidence independence: why three copies are not three reports
#
# Terms (GLOSSARY.md): prior odds, likelihood ratio, posterior odds, conditional independence,
# origin, derivative, double counting.
#
# **Purpose.** When several evidence items agree, how much should belief move? The answer
# depends on whether the items are conditionally independent given the claim, or copies of one
# origin.
#
# Run this file as a notebook in VS Code (`# %%` cells) or `uv run python notebooks/01_evidence_independence.py`.

# %%
from epistemic_lab.bayes import Report, likelihood_ratio, odds, posterior_naive, posterior_provenance_aware, prob

# %% [markdown]
# ## Step 1. One origin with reliability r = 0.8
#
# An origin reports the truth with probability 0.8. If it reports "claim true":
#
# LR = P(report true | H) / P(report true | not H) = 0.8 / 0.2 = 4.

# %%
print("LR(true report, r=0.8) =", likelihood_ratio(0.8, True))
print("LR(false report, r=0.8) =", likelihood_ratio(0.8, False))

# %% [markdown]
# ## Step 2. Prior 0.5 and one report
#
# prior odds = 1. posterior odds = 1 * 4 = 4. posterior probability = 4 / 5 = 0.80.

# %%
one = [Report("o1", 0.8, True)]
print("posterior after one report:", posterior_naive(0.5, one))

# %% [markdown]
# ## Step 3. Three independent reports: odds 1 * 4 * 4 * 4 = 64 -> 64/65

# %%
three_independent = [Report("o1", 0.8, True), Report("o2", 0.8, True), Report("o3", 0.8, True)]
print("three independent, naive:", round(posterior_naive(0.5, three_independent), 4))
print("three independent, aware:", round(posterior_provenance_aware(0.5, three_independent), 4))

# %% [markdown]
# ## Step 4. Three copies of one report
#
# A naive updater multiplies 4 three times and reaches 0.985. A provenance-aware updater
# multiplies once and stays at 0.80. The difference, 0.185, is the double-counting error.

# %%
three_copies = [Report("o1", 0.8, True), Report("o1", 0.8, True), Report("o1", 0.8, True)]
naive = posterior_naive(0.5, three_copies)
aware = posterior_provenance_aware(0.5, three_copies)
print("three copies, naive:", round(naive, 4))
print("three copies, aware:", round(aware, 4))
print("double-counting error:", round(naive - aware, 4))

# %% [markdown]
# ## Step 5. Why the copy adds nothing (the formal reason)
#
# Let E1 be the origin report and E2 a derivative. A derivative is a deterministic function of
# its parent: P(E2 | E1, H) = P(E2 | E1, not H) = 1. So the joint likelihood ratio is
#
#   P(E1, E2 | H) / P(E1, E2 | not H) = [P(E1|H) P(E2|E1,H)] / [P(E1|not H) P(E2|E1,not H)] = LR(E1).
#
# The multiplication rule LR(E1) * LR(E2) assumes P(E2 | E1, H) = P(E2 | H), which is false for a copy.

# %% [markdown]
# ## Step 6. How the error grows with the number of copies and with reliability

# %%
for r in (0.6, 0.8, 0.9):
    row = []
    for k in (1, 2, 3, 5):
        copies = [Report("o1", r, True)] * k
        row.append(round(posterior_naive(0.5, copies) - posterior_provenance_aware(0.5, copies), 3))
    print(f"r={r}: error for k=1,2,3,5 copies -> {row}")

# %% [markdown]
# ## Step 7. Connection to the review game
#
# In regime B (shared provenance), the presented items and both reviewers' private items are
# derivatives of one origin. A reviewer that counts items behaves like `posterior_naive`.
# A reviewer that counts origins behaves like `posterior_provenance_aware`. Hypothesis H-CORE-1
# predicts the false approval rate of naive agents rises in B relative to A. Run
# `uv run elab demo` to see the scripted version; the LLM run tests it on a model.
#
# ## Check yourself
# 1. With prior 0.5 and r = 0.8, what posterior do two independent true reports give? (16/17)
# 2. If one origin reports true and one derivative of a *different* origin reports false, what is the posterior? (0.5)
# 3. What assumption fails when two LLM reviewers were trained on the same corpus and read the same document?
