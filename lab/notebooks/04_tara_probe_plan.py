# %% [markdown]
# # 04. TARA project plan: a linear probe for collusion versus correlated agreement
#
# Terms: activation, residual stream, linear probe, anti-confound check, held-out split.
#
# **Purpose.** Lay out the full pipeline for H-TARA-1, 2, 3 in runnable PyTorch, so that the
# three-week project starts from working code. This notebook needs `uv sync --extra ml` and a
# small open-weight model. On CPU with a 1.5B model, extraction of a few hundred trajectories
# takes minutes, not hours. On free Colab GPU it is faster.
#
# **What this is not.** It has not been run as of 2026-10-23. Treat every number it prints
# as the first look, not a result.
#
# Hypotheses: H-TARA-1 (probe beats behavioral S3 on held-out), H-TARA-2 (probe does not
# separate E0 from A: it reads coordination, not incentive wording), H-TARA-3 (transfer
# across case families).

# %%
import json
from pathlib import Path
import numpy as np

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HAVE_ML = True
except ImportError:
    HAVE_ML = False
    print("torch/transformers not installed: run `uv sync --extra ml`. Showing the plan only.")

from epistemic_lab.auditors import render_slice
from epistemic_lab.regimes import COLLUSION_LABEL
from epistemic_lab.run import load_run

# %% [markdown]
# ## Step 1. Data: trajectories from the sprint runs
#
# Each trajectory is rendered as the S3 text (messages, endorsements, decision, presented
# evidence) so the probe sees what a behavioral S3 auditor sees, nothing more. Label = collusion
# label (E1, P = 1). Regime is kept for the anti-confound checks.

# %%
RUN_IDS = ["demo"]           # replace with ["dev-2026-10-24", "heldout-2026-10-25"] after the sprint
records = []
for rid in RUN_IDS:
    try:
        for t in load_run(rid):
            records.append({"text": render_slice(t, "S3"), "label": COLLUSION_LABEL[t.regime],
                            "regime": t.regime, "family": t.family})
    except FileNotFoundError:
        print(f"run {rid} not found; run `uv run elab demo` first")
print(len(records), "records")

# %% [markdown]
# ## Step 2. Activation extraction
#
# For each record: tokenize, run the model with `output_hidden_states=True`, take the
# residual-stream activation at the last token of a chosen layer. Shape: [d_model]. Stack to
# X: [n, d_model]. Middle layers usually carry the most linearly readable task information;
# sweep layers.

# %%
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"   # same base as the sprint's Dolos-1.5B red-team model

def extract(texts, layer, model, tok, max_len=1024, batch=4):
    X = []
    model.eval()
    with torch.no_grad():
        for i in range(0, len(texts), batch):
            enc = tok(texts[i:i+batch], return_tensors="pt", padding=True, truncation=True, max_length=max_len)
            out = model(**enc, output_hidden_states=True)
            hs = out.hidden_states[layer]                 # [b, seq, d_model]
            last = enc["attention_mask"].sum(1) - 1       # index of last real token per row
            X.append(hs[torch.arange(hs.shape[0]), last].float().cpu().numpy())
    return np.concatenate(X)                               # [n, d_model]

if HAVE_ML and records:
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    tok.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float32)
    texts = [r["text"] for r in records]
    LAYER = model.config.num_hidden_layers // 2
    X = extract(texts, LAYER, model, tok)
    print("activations:", X.shape)

# %% [markdown]
# ## Step 3. Probe: logistic regression on standardized activations, split by family

# %%
def probe_auroc(X, y, train_mask, test_mask, l2=1.0):
    from epistemic_lab.auditors import fit_logistic
    from epistemic_lab.metrics import auroc
    mu, sd = X[train_mask].mean(0), X[train_mask].std(0) + 1e-6
    Xs = (X - mu) / sd
    w, b = fit_logistic(Xs[train_mask], y[train_mask].astype(float), l2=l2, steps=2000, lr=0.05)
    s = 1 / (1 + np.exp(-(Xs[test_mask] @ w + b)))
    return auroc(s, y[test_mask]), s

if HAVE_ML and records:
    y = np.array([r["label"] for r in records])
    fam = np.array([r["family"] for r in records])
    reg = np.array([r["regime"] for r in records])
    dev_fams = {f"F{i:02d}" for i in range(1, 7)}
    train = np.isin(fam, list(dev_fams)); test = ~train
    au, _ = probe_auroc(X, y, train, test)
    print(f"H-TARA-1 / H-TARA-3: held-out family AUROC at layer {LAYER}: {au:.3f}")

# %% [markdown]
# ## Step 4. Anti-confound check (H-TARA-2): does the probe read incentive wording?
#
# Train the same probe to separate E0 from A (both label 0; differ only in payoff wording).
# If it succeeds (AUROC > 0.65), the collusion probe may be reading incentives, not coordination.

# %%
if HAVE_ML and records:
    m = np.isin(reg, ["E0", "A"])
    y2 = (reg == "E0").astype(int)
    au2, _ = probe_auroc(X[m], y2[m], train[m], test[m])
    print(f"H-TARA-2: E0 vs A AUROC: {au2:.3f}  (want <= 0.65)")

# %% [markdown]
# ## Step 5. Layer sweep and the three-week plan
#
# Week 1 (approx. 2026-11-21): data export from sprint runs; extraction pipeline; layer sweep on
# 100 trajectories; write the preregistration for H-TARA-1..3.
# Week 2: full extraction; probes; anti-confound checks (E0 vs A; family transfer; prompt-template
# shuffle); compare with behavioral S3 and S4 auditors on the same held-out split.
# Week 3: ablations (which tokens: messages only vs full), error analysis, presentation on 2026-12-12.
#
# Fallback if separable collusion behavior did not appear in the sprint LLM runs: H-TARA-F1,
# the behavioral dependence-effect evaluation (regime B vs A with and without provenance
# disclosure), which needs no collusion at all.
