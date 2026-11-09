"""v8 figures (2026-11-09): the v7 logic and numbers, the v5 cleanliness: one-line titles, one-line axis labels, short row labels; provenance and footnotes live in captions.md.
Draft-7 figures for the ARC-AGI-3 paper-track submission (2026-10-28).
House style carried from v6 (runs/paper-figures/v6 or docs/arc/paper/figures/v6/paper_figures_v6.py):
white background, font.size 9, top/right spines off, dark green #1f7a4d positive, dark red #b3382c
negative, grey #6b7772 nulls, black zero line, caption lines under the x-axis, dpi 180.
Data: pod mirrors runs/field/pod-mirror/<mirror>/benchmark.json wherever the number lives there
(RHAE/levels per the rhae_pair_read.py convention: per-game means over passes, mean over games;
tokens = median completion_tokens per game from *_requests.jsonl); campaign aggregates hardcoded
with the register row (runs/ledger/bets.json) named in the comment.

Usage: python3 paper_figures_v7.py          # titled PNGs with under-axis caption lines (markdown/web)
       python3 paper_figures_v7.py --paper  # Memento-style: no in-figure title, no caption lines;
                                            # graphics only, units on the axis labels; -> paper/F1.png..F5.png
                                            # (companion captions in captions.md carry title + provenance)
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, os, sys
PAPER = "--paper" in sys.argv
BASE = os.path.dirname(os.path.abspath(__file__))          # sits in runs/paper-figures/v8/
OUT = os.path.join(BASE, "paper") if PAPER else BASE
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
GREEN, RED, GREY, BROWN, CAP = "#1f7a4d", "#b3382c", "#6b7772", "#a86a00", "#5d6b64"
def save(fig, tag, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{tag if PAPER else name}.png", dpi=180, bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- F1: adoption channels, grouped by unit
groups = [  # (group label, [ (row label, point, lo, hi, note) ])
 ("RHAE", [
  ("Own cards, cross-day (B1b)", 5.5, 1.2, 10.1, ""),   # row 18 §362: +5.53, 90% [+1.22,+10.10]
  ("Own cards, same-day replication 1", -0.3, -4.15, 3.55, ""),  # row cards-same-day-pair §364: -0.30 ± 2.34, 90% ±3.85
  ("Own cards, same-day replication 2", -2.86, -5.87, 0.15, ""),  # row cards-same-day-pair-3 §370: -2.86 ± 1.83, 90% ±3.0
  ("Own cards, three reads pooled", -0.2, -2.3, 1.9, ""),            # inverse-variance: -0.21 ± 1.27, 90% ±2.1
  ("Own cards, MiMo V2.6 Flash", -0.14, -3.5, 3.2, ""),   # row mimo-cards-pair-25: -0.14 ± 2.06
  ("Own cards, three families pooled", -0.33, -1.7, 1.0, ""),      # Part IIb: -0.33 ± 0.83, 90% [-1.7, +1.0]
  ("Own notes above the line (GPT-6.1 Sol, open)", 1.9, -8.9, 12.8, ""),  # Part IIb: +1.9 ± 6.6
 ]),
 ("levels/25", [
  ("Verified own cards (A1)", 1.2, -9.2, 11.8, ""),                          # row 88
  ("Harness rulebook (O1)", -8, -24, 7, ""),                                       # row 60 §236a
  ("Effect ledger (L1)", -9, -23, 4, ""),                   # row 43
  ("Cards from an earlier run (B1d)", -8.6, -12.6, -4.5, ""),          # row 21: -8.61 [-12.6,-4.5]
  ("Bigger blocks (B1c)", -3.95, -7.11, -0.53, ""),                        # row 20
  ("Policy mixes (B1e)", -4.69, -7.5, -1.9, ""),                                   # row 22: [-7.5,-1.9]
  ("Manuals, other games (P3)", -6, -12, 0, ""),                             # row 83: -6 over 20 games; ±6 per brief
 ]),
 ("levels/5 games", [
  ("Same-game manual (R1)", 0, -5, 5, ""),                              # row 109: 10 vs 10 levels
  ("Own cards, Mercury 3", 0.6, -0.6, 1.8, ""),               # row 129: RHAE +0.61 ± 1.16 (RHAE units)
 ]),
]
rows = [r for _, rs in groups for r in rs]
fig, ax = plt.subplots(figsize=(7.2, 5.0))
gap = 0.9  # extra vertical space between unit groups
y, cur = [], 0.0
for glab, rs in groups:
    for _ in rs:
        y.append(cur); cur -= 1.0
    cur -= gap
y = np.array(y)  # rows listed top -> bottom; first row highest
for yi, (lab, p, lo, hi, note) in zip(y, rows):
    c = GREEN if lo > 0 else (RED if hi < 0 else GREY)
    ax.errorbar(p, yi, xerr=[[p - lo], [hi - p]], fmt="o", color=c, capsize=3)
# group separators + unit labels
bounds, start = [], 0
for glab, rs in groups:
    idx = np.arange(start, start + len(rs))
    bounds.append((glab, y[idx[0]], y[idx[-1]]))
    start += len(rs)
for i in range(len(bounds) - 1):
    ax.axhline((bounds[i][2] + bounds[i + 1][1]) / 2, color="#c8cfcc", lw=0.7, ls="--")
for glab, ytop, ybot in bounds:
    ax.text(19.3, (ytop + ybot) / 2, f"unit: {glab}", va="center", fontsize=7.5, color=CAP, style="italic")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows])
ax.axvline(0, color="k", lw=0.8)
ax.set_xlim(-26, 19); ax.set_ylim(y[-1] - 0.7, y[0] + 0.7)
if PAPER:
    ax.set_xlabel("paired effect vs control, 90% intervals")
else:
    ax.set_xlabel("paired effect vs control, 90% interval")
    ax.set_title("Fig. 1  Does the loop reach the score? Own notes and handed structure, paired against controls", loc="left", fontsize=9.5)
save(fig, "F1", "F1-adoption-channels")

# ---------------------------------------------------------------- F3: the budget curve with the same-day pair
# Cross-day stock reads, exact from the pod mirrors (median completion tokens/game, mean RHAE):
reads = [  # (label, K tokens/game median, RHAE)  <- runs/field/pod-mirror/<mirror>/benchmark.json + *_requests.jsonl
 ("capc 10-21", 158.8, 39.80),   # 2026-10-21-capc:   RHAE 39.80, med 158.8K, levels 98
 ("ctl 10-25", 158.9, 33.41),    # 2026-10-25-rung1ctl: RHAE 33.41, med 158.9K, levels 87
 ("p2c 10-14", 530.9, 62.81),    # 2026-10-14-p2c:    RHAE 62.81, med 530.9K
 ("s7ac 10-15", 502.0, 62.00),   # 2026-10-15-s7ac:   RHAE 62.00, med 502.0K
 ("t1c 10-17", 608.3, 67.78),    # 2026-10-17-t1c:    RHAE 67.78, med 608.3K
 ("knoba 10-18", 521.4, 65.46),  # 2026-10-18-knoba:  RHAE 65.46, med 521.4K
 ("knobr 10-18", 456.4, 64.24),  # 2026-10-18-knobr:  RHAE 64.24, med 456.4K
]
budgA = (158.7, 35.72)  # 2026-10-28-budgA: RHAE 35.72, med 158.7K (register row 122: 35.72, 159K)
budgB = (543.0, 71.46)  # 2026-10-28-budgB: RHAE 71.46, med 543.0K (register row 122: 71.46, 543K)
# row 122: +35.74 ± 5.75; 3.68x tokens (ratio of per-game means 566.4/154.1; medians 543/159 = 3.42);
# elasticity in RHAE 0.53 [90% game-clustered bootstrap 0.37, 0.75]
x = np.array([r[1] for r in reads]); yv = np.array([r[2] for r in reads])
b, a = np.polyfit(np.log(x), np.log(yv), 1)   # cross-day log-log slope ~0.47
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.scatter(x, yv, color=GREY, s=28, zorder=4)
laboff = {"capc 10-21": (-6, 4, "right"), "ctl 10-25": (-6, -4, "right"), "p2c 10-14": (7, -2, "left"),
          "s7ac 10-15": (-6, -14, "right"), "t1c 10-17": (7, -2, "left"), "knoba 10-18": (8, -2, "left"),
          "knobr 10-18": (-6, 8, "right")}

xs = np.linspace(140, 680, 60)
ax.plot(xs, np.exp(a) * xs**b, color="#9aa7a1", lw=1, ls="--", label=f"cross-day stock reads (log-log slope {b:.2f})")
ax.plot([budgA[0], budgB[0]], [budgA[1], budgB[1]], color=GREEN, lw=3, zorder=5)
ax.scatter(*budgA, color=GREEN, s=90, zorder=6); ax.scatter(*budgB, color=GREEN, s=90, zorder=6)
ax.annotate("3.7× tokens: 36 → 72, elasticity 0.53 [0.37, 0.75]", xy=(300, 56), xytext=(235, 73), fontsize=8, color=GREEN, ha="center",
            arrowprops=dict(arrowstyle="-", lw=0.6, color=GREEN))
b1x = (159.6, 33.48)  # 2026-10-29-b1x: RHAE 33.48, median 159.6K (row budget-pair-2x)
b2x = (316.5, 52.74)  # 2026-10-29-b2x: RHAE 52.74, median 316.5K; +19.25 ± 5.41; elasticity RHAE 0.83 [0.63, 1.01] (means 1.73×)
ax.plot([b1x[0], b2x[0]], [b1x[1], b2x[1]], color=GREEN, lw=3, zorder=5, alpha=0.75)
ax.scatter(*b1x, color=GREEN, s=80, zorder=6, marker="s"); ax.scatter(*b2x, color=GREEN, s=80, zorder=6, marker="s")
ax.annotate("1.7× tokens: 33 → 53, elasticity 0.83 [0.63, 1.01]", xy=(255, 46.5), xytext=(330, 38), fontsize=8, color=GREEN, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.6, color=GREEN))
ax.axvline(158, color=RED, lw=0.8, ls=":")
ax.text(154, 77.5, "Kaggle budget", fontsize=7.5, color=RED, ha="right", va="top")
ax.set_xscale("log"); ax.set_xlim(130, 720); ax.set_ylim(28, 80)
ax.xaxis.set_minor_formatter(plt.NullFormatter()); ax.set_xticks([158, 300, 500, 700])
ax.set_xticklabels(["158", "300", "500", "700"])
ax.set_xlabel("generated tokens per game (K, log scale)")
ax.set_ylabel("public RHAE (25 games)")
ax.legend(loc="lower right", fontsize=7.5, frameon=False)
if not PAPER: ax.set_title("Fig. 2  Thinking time buys score: two same-day pairs, diminishing", loc="left")
save(fig, "F3", "F3-budget-curve")

# ---------------------------------------------------------------- F4: the discriminator, standalone
# Register (screen data not mirrored locally): row 132 (Astra 174/217), row 56 §233 (Sol 16 [12,20]),
# row 111 screen23 (DeepSeek 3, MiMo 4, Nemotron 1, Qwen 0), row 107 (Mercury 3 off: 3),
# row 56 (Flash-Next no-thinking: 1); market screen rows screen24-* (2026-11-04/05). 90% bootstrap intervals per v6/brief; Wilson for the 11-04 rows.
disc = [  # (label, point, lo, hi)
 ("GPT-6 Astra*", 174/217*23, 160/217*23, 185/217*23),   # row 132: 174/217 -> ~19 [17,20] scaled to 23 cells
 ("GPT-6.1 Terra", 20, 16, 22),                # row screen24-terra: 20/23; 90% Wilson interval on 23 cells
 ("GPT-6.1 Sol", 16, 12, 20),                             # row 56 §233: 16/23, 90% game-bootstrap [12,20]
 ("MiMo V2.6 Flash", 4, 1, 7),                            # row 111: 4/23 (brief said 3 [1,5]; register says 4/23)
 ("Mercury 3", 3, 1, 5),                  # row 107: 3 beats
 ("DeepSeek V4.1 Flash", 3, 1, 5),                        # row 111: 3/23
 ("DeepSeek V4 Pro", 3, 1, 7),    # rows screen24-dsv4pro / -48k: 2, 2 at 24K and 3 at 48K, a third of iterations cut each time; 0 with reasoning off
 ("Grok 4.3", 1, 0, 4),                                   # row screen24-grok43: 1/23 clean
 ("GPT-6 Luna Pro", 1, 0, 4),                             # row screen24-luna-pro: 1/23 clean
 ("MiMo V2.6 Pro", 1, 0, 4),              # row screen24-mimo-pro: 1/23
 ("Nemotron 3.5 Super", 1, 0, 4),                         # row 111: 1/23
 ("Flash-Next (ours)", 1, 0, 3),           # row 56: 1/23
 ("Qwen3.8-27B", 0, 0, 0),                                # row 111: 0/23
 ("Luna, Haiku 5.5, Kimi K2, GLM-5.1, Grok Build", 0, 0, 0),   # rows screen24-*: 0/23 clean reads
]
fig, ax = plt.subplots(figsize=(7.2, 5.6))
yy = np.arange(len(disc))[::-1]
for yi, (lab, p, lo, hi) in zip(yy, disc):
    c = GREEN if p >= 8 else GREY
    if hi > lo:
        ax.errorbar(p, yi, xerr=[[p - lo], [hi - p]], fmt="o", color=c, capsize=3)
    else:
        ax.scatter(p, yi, color=c, s=40, zorder=5)
ax.set_yticks(yy); ax.set_yticklabels([d[0] for d in disc], fontsize=8.5)
ax.axvline(8, color=RED, lw=0.8, ls=":")
ax.text(8.25, len(disc) - 0.45, "bar: 8 of 23", fontsize=8, color=RED)
ax.set_xlim(-0.7, 22.8); ax.set_ylim(-0.7, len(disc) - 0.1)
if PAPER:
    ax.set_xlabel("cells beating nothing-changes (of 23)")
else:
    ax.set_xlabel("cells where the model's program beats the no-change baseline (of 23, 90% interval)")
    ax.set_title("Fig. 3  The gate: who can write a replay-exact simulator of a level", loc="left")
save(fig, "F4", "F4-discriminator")

# ---------------------------------------------------------------- F5: the design-law map (schematic)
# Measured anchors: probe scores rows 56/107/111/132; structure effects (own cards pooled −0.2),
# 109 (R1 0), 129 (mercury3 +0.6), 83/60/43 (P3/O1/L1 null-to-negative); frontier band from the
# ceiling papers (Memento 3 = 100; Tycho/Twin/Kepler 93-100; draft6 §5).
fig, ax = plt.subplots(figsize=(7.2, 4.6))
rng = np.random.default_rng(7)
openx = [0, 1, 1, 3, 3, 4]                        # Qwen 0, Nemotron 1, Flash-Next 1, Mercury 3, DeepSeek 3, MiMo 4
openy = [0.0, 0.6, -0.5, 0.3, -0.3, 0.2]          # structure effect ~ 0 (R1 0; mercury +0.6; rest null)
ax.scatter(openx, openy, color=GREY, s=34, zorder=5)
ax.scatter([1], [-0.2], color=GREY, s=70, zorder=6)                    # own cards on Flash-Next: three four-pass reads pooled -0.2 ± 1.3
ax.annotate("own notes: no effect\n(−0.2 ± 1.3 pooled; ±1.7 over three families)", (1, -0.2), xytext=(4, 14), textcoords="offset points",
            fontsize=7.5, color=GREY)
ax.scatter([20], [1.9], color=GREY, s=42, zorder=5, marker="D")        # GPT-6.1 Sol own notes: +1.9 ± 6.6 (open); x = Terra/Sol probe band
ax.annotate("own notes above the line:\n+1.9 ± 6.6, open", (20, 1.9), xytext=(-10, -30), textcoords="offset points", fontsize=7.5, color=GREY, ha="right")
front = [("Kepler", 16, 99), ("Twin", 17.4, 93.3), ("Tycho", 18, 97), ("Memento 3", 19, 100)]
for lab, fx, fy in front:
    ax.scatter(fx, fy, color=GREY, s=42, zorder=5)
ax.annotate("Memento 3 = 100", (19, 100), xytext=(0, 10), textcoords="offset points", fontsize=7.5, ha="center")
ax.annotate("Tycho / Twin / Kepler: 93–100", (17.4, 93.3), xytext=(6, -13), textcoords="offset points", fontsize=7.5, color="#3f4a45")
ax.axvspan(-0.8, 8, color="#f4f6f5", zorder=0); ax.axvspan(8, 21.2, color="#eef3f0", zorder=0)
ax.axvline(8, color=GREY, lw=0.9, ls="--")
ax.text(8, 106, "the line: bar 8 of 23 (the probe places a model in one hour)", fontsize=7.5, color="#3f4a45", ha="center")
ax.axhline(0, color="k", lw=0.8)
ax.text(3.8, 62, "below the line: nothing delivered\nconverts; thinking time does", fontsize=8, ha="center", va="top",
        color="#3f4a45", linespacing=1.5)
ax.text(15.2, 62, "above the line: structure is used\n(the ceiling papers)", fontsize=8, ha="center", va="top",
        color="#3f4a45", linespacing=1.5)
ax.text(3.4, -16, "handed structure reads null:\nrulebooks, manuals, tools, facts", fontsize=7.5,
        color=GREY, ha="center", va="top", style="italic", linespacing=1.5)
ax.set_xlim(-0.8, 21.2); ax.set_ylim(-30, 110)
ax.set_xlabel("probe score (cells of 23)")
ax.set_ylabel("RHAE with harness structure\n(below the line: effect; above: RHAE reached)")
if not PAPER: ax.set_title("Fig. 4  The map: where written help reaches a model (schematic)", loc="left")
save(fig, "F5", "F5-design-law-map")

print(f"figures written to {OUT}:", sorted(f for f in os.listdir(OUT) if f.endswith(".png")))
