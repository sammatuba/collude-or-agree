# %% [markdown]
# # 02. The review game with scripted agents
#
# Terms: proposer, reviewer, decider, regime, trajectory, invalid approval, positive control,
# negative control, communication effect.
#
# **Purpose.** See one trajectory end to end, then the whole regime table, with agents whose
# rules we wrote. Nothing here costs API credit.

# %%
from epistemic_lab.agents import scripted_roster
from epistemic_lab.game import run_trajectory
from epistemic_lab.regimes import REGIMES, WHAT_IT_ISOLATES
from epistemic_lab.run import audit, print_report
from epistemic_lab.cases import FAMILIES, all_case_specs
import json

# %% [markdown]
# ## Step 1. One trajectory in regime P (certain collusion, scripted)

# %%
t = run_trajectory("F01", False, "P", scripted_roster("P"), seed=0)
print("claim:", t.claim.text, "| truth:", t.truth)
print("presented:", t.presented)
for m in t.messages:
    print(f"[{m.channel}] {m.sender}->{m.to}: {m.text}")
for k, e in t.endorsements.items():
    print(k, e.vote, e.cited, "|", e.reason)
print("decision:", t.decision, "| invalid approval:", t.invalid_approval)
print("payoffs:", t.payoffs)

# %% [markdown]
# ## Step 2. The same case and seed in regime E0 (same incentives, no channel)
#
# E0 is the counterfactual for P: identical world draw, identical selective proposer, eager
# reviewers, but no private message. Compare the endorsements.

# %%
t0 = run_trajectory("F01", False, "E0", scripted_roster("E0"), seed=0)
for k in t.endorsements:
    print(k, "P:", t.endorsements[k].vote, t.endorsements[k].cited, "| E0:", t0.endorsements[k].vote, t0.endorsements[k].cited)
print("P decision", t.decision.action, "| E0 decision", t0.decision.action)

# %% [markdown]
# ## Step 3. Every regime, every case, several seeds

# %%
trajs = []
for fam, truth in all_case_specs([f.family_id for f in FAMILIES]):
    for seed in range(5):
        for r in REGIMES:
            if r == "E1":
                continue  # scripted E1 is identical to P
            trajs.append(run_trajectory(fam, truth, r, scripted_roster(r), seed))
rep = audit(trajs, n_boot=300)
print_report(rep, "scripted, 5 seeds")

# %% [markdown]
# ## Step 4. Read the table
#
# - FAR(B) > FAR(A): the naive decider and reviewers double count derivatives (H-CORE-1).
# - FAR(E0) > FAR(A): parallel conduct harms without any coordination (H-SPRINT-5).
# - S1 flags F at 100 percent: talk fools a messages-only auditor (H-SPRINT-1).
# - S2 cannot separate E0 from P: harmful agreement looks the same (H-SPRINT-2).
# - S4 keeps P at 100 percent and drops F, B, C: innocent explanations are discounted (H-SPRINT-3).
#
# These are design checks on scripted agents, not findings about language models.
#
# ## Check yourself
# 1. Why is FAR(P) well below 1.0 even though the coalition always coordinates?
# 2. Which feature lets S4 reject F while S3 accepts it? What would a deployed auditor lack?
# 3. What would you expect to change in this table if the reviewers were LLMs with accuracy-aligned prompts?
