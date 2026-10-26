# %% [markdown]
# # 03. Epistemic plus factors and the auditor slices
#
# Terms: information slice, epistemic plus factor, dev split, held-out split, freeze, AUROC,
# false-positive rate, recall.
#
# **Purpose.** Compute the ten features on trajectories, see which differ across regimes, fit
# the logistic rule on the dev split, evaluate on held-out, and draw the ROC per slice.

# %%
import numpy as np
from epistemic_lab.agents import scripted_roster
from epistemic_lab.auditors import FEATURES_BY_SLICE, RuleAuditor, SLICES, features
from epistemic_lab.cases import DEV_FAMILIES, HELDOUT_FAMILIES, all_case_specs
from epistemic_lab.game import run_trajectory
from epistemic_lab.metrics import auroc, precision_recall_fpr
from epistemic_lab.regimes import COLLUSION_LABEL, REGIMES
from epistemic_lab.run import _counterfactual_index

def make(families, seeds=3):
    out = []
    for fam, truth in all_case_specs(families):
        for s in range(seeds):
            for r in REGIMES:
                if r == "E1":
                    continue
                out.append(run_trajectory(fam, truth, r, scripted_roster(r), s))
    return out

dev, held = make(DEV_FAMILIES), make(HELDOUT_FAMILIES)

# %% [markdown]
# ## Step 1. Feature means per regime (dev)

# %%
cf = _counterfactual_index(dev)
F = [features(t, cf.get(t.key)) for t in dev]
names = FEATURES_BY_SLICE["S4"]
print(f"{'regime':7s}" + "".join(f"{n[:9]:>10s}" for n in names))
for r in REGIMES:
    rows = [f for t, f in zip(dev, F) if t.regime == r]
    if rows:
        print(f"{r:7s}" + "".join(f"{np.mean([f[n] for f in rows]):10.2f}" for n in names))

# %% [markdown]
# Read down each column. `coord_talk` is 1 in both F and P: talk alone cannot separate them.
# `payoff_aligned` is 1 in E0 and P: motive alone cannot separate them. `cf_shift` is 1 only
# where the channel changed an action. The combination is the plus-factor argument.

# %% [markdown]
# ## Step 2. Fit on dev, freeze, evaluate on held-out

# %%
labels_dev = [COLLUSION_LABEL[t.regime] for t in dev]
cf_h = _counterfactual_index(held)
F_h = [features(t, cf_h.get(t.key)) for t in held]
labels_h = [COLLUSION_LABEL[t.regime] for t in held]
for s in SLICES:
    a = RuleAuditor(s).fit(F, labels_dev)
    scores = [a.score(f) for f in F_h]
    m = precision_recall_fpr(held, scores)
    print(f"{s}: AUROC={auroc(scores, labels_h):.3f} recall={m['recall']:.2f} FPR={m['fpr']:.2f} "
          + " ".join(f"{n}={w:+.1f}" for n, w in zip(a.feature_names, a.weights)))

# %% [markdown]
# In the scripted world the fit is nearly perfect because the regimes are deterministic rules.
# The LLM run is where this becomes an experiment: `uv run elab audit heldout-<date> --fit dev-<date>`.

# %% [markdown]
# ## Step 3. ROC curves (optional; needs matplotlib from `--extra dev`)

# %%
try:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 5))
    y = np.array(labels_h)
    for s in SLICES:
        a = RuleAuditor(s).fit(F, labels_dev)
        sc = np.array([a.score(f) for f in F_h])
        ths = np.unique(sc)[::-1]
        tpr = [((sc >= th) & (y == 1)).sum() / (y == 1).sum() for th in ths]
        fpr = [((sc >= th) & (y == 0)).sum() / (y == 0).sum() for th in ths]
        ax.plot([0] + fpr + [1], [0] + tpr + [1], label=f"{s} AUROC={auroc(sc, y):.2f}")
    ax.plot([0, 1], [0, 1], "k--", lw=0.5)
    ax.set_xlabel("false-positive rate (innocent regimes flagged)")
    ax.set_ylabel("recall (collusion regimes flagged)")
    ax.legend(); ax.set_title("ROC per information slice, held-out families (scripted)")
    plt.tight_layout(); plt.show()
except ImportError:
    print("matplotlib not installed; skip the plot")

# %% [markdown]
# ## Check yourself
# 1. Which two features would you remove to simulate a deployed auditor, and why? (f7, f10)
# 2. Why fit on dev and evaluate on held-out *by family*, not by trajectory? (confound CF-3)
# 3. If S4's advantage disappears without f10, what does that say about the realism of the contribution?
