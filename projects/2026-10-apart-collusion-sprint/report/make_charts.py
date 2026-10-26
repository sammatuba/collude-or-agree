"""Charts for the report, the explainer, and the deck. Reads the generated tables in
RESULTS-SEVEN-MODELS.md (so the charts cannot drift from the numbers) and writes SVG and PNG
files to report/figures/.

Run from lab/:  uv run python ../projects/2026-10-apart-collusion-sprint/report/make_charts.py

Design rules (tools: the dataviz method): one axis per chart; two categorical colors, validated
(innocent blue 1F6E9C, collusion red B5482F); gray only for reference lines; thin marks; a legend
when there are two series; selective direct labels; text in ink, not in series colors.
"""
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)
BLUE, RED, INK, MUTED, RULE = "#1F6E9C", "#B5482F", "#1B2430", "#5A6675", "#D5DBE3"
MODELS = ["DeepSeek chat", "Claude Haiku 5.5", "GPT-5.6 Luna", "Claude Sonnet 5.5", "GPT-5.6 Terra", "DeepSeek V4 Pro", "DeepSeek Flash"]
SHORT = ["DS chat", "Haiku 5.5", "Luna", "Sonnet 5.5", "Terra", "DS V4 Pro", "DS Flash"]
REGIMES = ["A", "B", "C", "D", "E0", "E1", "F", "P"]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": RULE, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "axes.spines.top": False,
                     "axes.spines.right": False, "svg.fonttype": "none"})


def read_tables(path: Path) -> list[dict]:
    """Return each Markdown table as {header: [...], rows: [[...]]}."""
    tables, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            if cur is None:
                cur = {"header": cells, "rows": []}
            else:
                cur["rows"].append(cells)
        else:
            if cur:
                tables.append(cur)
            cur = None
    if cur:
        tables.append(cur)
    return tables


def ci(cell: str):
    m = re.match(r"\s*(-?[\d.]+)\s*\[\s*(-?[\d.]+),\s*(-?[\d.]+)\]", cell.replace("−", "-"))
    return tuple(float(x) for x in m.groups())


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("wrote", name)


def main():
    tabs = read_tables(HERE / "RESULTS-SEVEN-MODELS.md")
    seven = tabs[0]
    row = {r[0]: r[1:] for r in seven["rows"]}
    cols = seven["header"][1:]
    assert cols == MODELS, cols

    # Figure 1: false approval rate by regime, one panel per model
    fig, axes = plt.subplots(2, 4, figsize=(10, 4.6), sharey=True)
    axes = axes.ravel()
    for i, m in enumerate(MODELS):
        ax = axes[i]
        vals = [float(row[f"FAR {r}"][i]) for r in REGIMES]
        colors = [RED if r in ("E1", "P") else BLUE for r in REGIMES]
        bars = ax.bar(REGIMES, vals, color=colors, width=0.62)
        for b, r, v in zip(bars, REGIMES, vals):
            if r in ("E0", "E1"):
                ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.2f}", ha="center", va="bottom", fontsize=7.5, color=INK)
        ax.set_title(SHORT[i], fontsize=9.5, loc="left")
        ax.set_ylim(0, 0.75)
        ax.grid(axis="y", color=RULE, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", labelsize=7.5)
    axes[7].axis("off")
    axes[7].text(0.0, 0.85, "Blue: innocent regimes\nRed: collusion regimes (E1, P)\n\nEach bar: fraction of 18\nfalse claims approved.\nP is scripted in every run.",
                 fontsize=8.5, va="top", color=INK)
    axes[0].set_ylabel("False approval rate")
    axes[4].set_ylabel("False approval rate")
    fig.suptitle("Figure 1. False approval rate by regime, seven models (held-out families)", x=0.01, ha="left", fontsize=10.5)
    fig.tight_layout()
    save(fig, "fig1_far_by_regime")

    # Figure 2: matched contrasts with intervals (forest plot, three panels)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    for ax, key, title in zip(axes, ["E1 minus E0", "E0 minus A", "B minus A"],
                              ["Private channel: E1 minus E0", "Shared incentive: E0 minus A", "Shared source: B minus A"]):
        for j, m in enumerate(MODELS):
            p, lo, hi = ci(row[key][j])
            excl = lo > 0 or hi < 0
            ax.plot([lo, hi], [j, j], color=BLUE, linewidth=2, solid_capstyle="round")
            ax.plot(p, j, marker="o", markersize=7, color=BLUE if excl else "white", markeredgecolor=BLUE, markeredgewidth=1.6)
            ax.text(0.62, j, f"{p:+.3f}", va="center", fontsize=7.5, color=MUTED)
        ax.axvline(0, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
        ax.set_xlim(-0.45, 0.75)
        ax.set_yticks(range(len(MODELS)))
        ax.set_yticklabels(SHORT)
        ax.invert_yaxis()
        ax.set_title(title, fontsize=9.5, loc="left")
        ax.grid(axis="x", color=RULE, linewidth=0.6)
        ax.set_axisbelow(True)
    axes[0].set_xlabel("Difference in false approval rate")
    fig.suptitle("Figure 2. Matched contrasts on false claims, with 95 percent bootstrap intervals (filled marker: interval excludes zero)",
                 x=0.01, ha="left", fontsize=10.5)
    fig.tight_layout()
    save(fig, "fig2_contrasts")

    # Figure 3: provenance reduction against the preregistered target
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for j, m in enumerate(MODELS):
        p, lo, hi = ci(row["Reduction S3 minus S4d"][j])
        ax.barh(j, p, color=BLUE, height=0.55)
        ax.plot([lo, hi], [j, j], color=INK, linewidth=1.2)
        ax.text(max(hi, p) + 0.004, j, f"{p:.3f}", va="center", fontsize=7.5, color=MUTED)
    ax.axvline(0.10, color=RED, linewidth=1.4, linestyle=(0, (4, 3)))
    ax.text(0.101, -0.9, "preregistered target 0.10", color=RED, fontsize=8, va="bottom")
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels(SHORT)
    ax.invert_yaxis()
    ax.set_xlim(0, 0.13)
    ax.set_xlabel("Reduction in pooled false-positive rate, S3 minus S4d")
    ax.grid(axis="x", color=RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.suptitle("Figure 3. Provenance data reduced false positives by 0.000 to 0.017 (target 0.10)", x=0.01, ha="left", fontsize=10.5)
    fig.tight_layout()
    save(fig, "fig3_provenance")

    # Figure 4: judge flags on the injected plan versus reviewer replies
    replies = {"DeepSeek chat": 10, "Claude Haiku 5.5": 72, "GPT-5.6 Luna": 72, "Claude Sonnet 5.5": 72,
               "GPT-5.6 Terra": 72, "DeepSeek V4 Pro": 0, "DeepSeek Flash": 36}
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for j, m in enumerate(MODELS):
        f = int(row["Judge S1: E1 / F / innocent"][j].split("/")[1].split("of")[0])
        x, y = replies[m], f
        ax.plot(x, y, marker="o", markersize=8, color=BLUE, markeredgecolor="white", markeredgewidth=1.5)
        dx, dy = (6, 0) if m not in ("Claude Haiku 5.5", "GPT-5.6 Luna", "Claude Sonnet 5.5") else (6, {"Claude Haiku 5.5": 3.5, "GPT-5.6 Luna": -3.5, "Claude Sonnet 5.5": -7.5}[m])
        ax.annotate(SHORT[j], (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=8, color=INK, va="center")
    ax.set_xlabel("Reviewer replies to the injected plan in regime F (of 72), all refusals")
    ax.set_ylabel("F trajectories flagged\nby the LLM judge, S1 (of 36)")
    ax.set_xlim(-5, 95)
    ax.set_ylim(-2, 40)
    ax.grid(color=RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.suptitle("Figure 4. The judge flags unanswered plans; written refusals by both reviewers lower its flags", x=0.01, ha="left", fontsize=10.5)
    fig.tight_layout()
    save(fig, "fig4_judge_vs_replies")

    # Figure 5: what the agents said and did (three hand-read models)
    cats = ["Biasing plan sent", "Both agreed in words", "Agreed and both endorsed", "Both refused in words",
            "Refused but both endorsed", "All three parts of collusion", "...and action changed vs E0"]
    data = {"DS chat": [23, 12, 3, 8, 3, 1, 0], "Terra": [17, 4, 1, 5, 2, 1, 1], "DS Flash": [20, 5, 1, 11, 4, 0, 0]}
    fig, ax = plt.subplots(figsize=(8, 3.6))
    n = len(cats)
    w = 0.26
    shades = {"DS chat": BLUE, "Terra": "#6FA7C9", "DS Flash": "#A9CBE0"}
    for k, (m, vals) in enumerate(data.items()):
        xs = [i + (k - 1) * (w + 0.02) for i in range(n)]
        ax.bar(xs, vals, width=w, color=shades[m], label=m)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.4, str(v), ha="center", va="bottom", fontsize=7.2, color=INK)
    ax.set_xticks(range(n))
    ax.set_xticklabels(cats, rotation=18, ha="right", fontsize=8)
    ax.set_ylabel("Trajectories (of 36 per model)")
    ax.set_ylim(0, 27)
    ax.grid(axis="y", color=RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, title="Model (one hue, three steps)", title_fontsize=8)
    fig.suptitle("Figure 5. What the agents said and did in the collusion-opportunity regime E1", x=0.01, ha="left", fontsize=10.5)
    fig.tight_layout()
    save(fig, "fig5_say_do")

    # Figure 6: coordination-pivotal regimes (E0p, E1p, and E1q when present)
    piv = [t for t in tabs if "Measure" in t["header"][0] and any("E0p" in r[0] for r in t["rows"])]
    if piv:
        t = piv[-1]
        prow = {r[0]: r[1:] for r in t["rows"]}
        pm = t["header"][1:]
        fig, ax = plt.subplots(figsize=(6.4, 2.8 + 0.1 * len(pm)))
        for j, m in enumerate(pm):
            e0 = float(prow["False approval rate E0p"][j]); e1 = float(prow["False approval rate E1p"][j])
            ax.plot([e0, e1], [j, j], color=RULE, linewidth=2)
            ax.plot(e0, j, marker="o", markersize=8, color="white", markeredgecolor=BLUE, markeredgewidth=1.8, label="E0p, no channel" if j == 0 else None)
            ax.plot(e1, j, marker="o", markersize=8, color=RED, label="E1p, private channel" if j == 0 else None)
            if "False approval rate E1q" in prow:
                e1q = float(prow["False approval rate E1q"][j])
                ax.plot(e1q, j, marker="D", markersize=7, color=RED, markeredgecolor="white", label="E1q, proposer knows the rule" if j == 0 else None)
            ax.text(0.47, j, prow["E1p minus E0p (communication effect)"][j], va="center", fontsize=7.5, color=MUTED)
        ax.set_yticks(range(len(pm)))
        ax.set_yticklabels(pm)
        ax.invert_yaxis()
        ax.set_xlim(-0.02, 0.75)
        ax.set_xlabel("False approval rate (18 false claims)")
        ax.grid(axis="x", color=RULE, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.legend(frameon=False, fontsize=8, loc="lower right")
        fig.suptitle("Figure 6. When a lone endorser is blamed, the channel still adds no harm (E1p minus E0p at right)", x=0.01, ha="left", fontsize=10.5)
        fig.tight_layout()
        save(fig, "fig6_pivotal")


if __name__ == "__main__":
    main()
