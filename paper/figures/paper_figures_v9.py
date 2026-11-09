"""v9 figures (2026-11-09): Fig. 1 = the note system at work (outcome, and the writer test); Fig. 4 = the loop with its measurements; Figs. 2 and 3 as v8.
v8 figures (2026-11-09): the v7 logic and numbers, the v5 cleanliness: one-line titles, one-line axis labels, short row labels; provenance and footnotes live in captions.md.
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
BASE = os.path.dirname(os.path.abspath(__file__))          # sits in runs/paper-figures/v9/
OUT = os.path.join(BASE, "paper") if PAPER else BASE
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
GREEN, RED, GREY, BROWN, CAP = "#1f7a4d", "#b3382c", "#6b7772", "#a86a00", "#5d6b64"
def save(fig, tag, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{tag if PAPER else name}.png", dpi=180, bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- F1 (v9): the note system at work, two panels
fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
# left: does the model's own note reach the score (RHAE, 90% intervals; register rows B1b, cards-same-day(-3), mimo/mercury pools, sol-rep)
left = [("the first read", 5.5, 1.2, 10.1),
        ("replications, pooled", -0.2, -2.3, 1.9),
        ("three families, pooled", -0.33, -1.7, 1.0),
        ("a top model's notes (early read)", 1.9, -8.9, 12.8)]
yy = np.arange(len(left))[::-1]
for yi, (lab, p, lo, hi) in zip(yy, left):
    c = GREEN if lo > 0 else GREY
    axL.errorbar(p, yi, xerr=[[p - lo], [hi - p]], fmt="o", color=c, capsize=3)
    axL.text(hi + 0.5, yi, f"{p:+.1f}", fontsize=7.5, va="center", color=c)
axL.set_yticks(yy); axL.set_yticklabels([l[0] for l in left], fontsize=8.5)
axL.axvline(0, color="k", lw=0.8); axL.set_xlim(-10, 16)
axL.set_xlabel("paired effect on the score vs control (RHAE, 90%)")
axL.set_title("Do the notes reach the score?", loc="left", fontsize=9.5)
# right: does the model carry its note forward (writer test; released corpus, writer_consistency_paper.sh and the 11-09 split)
right = [("open model, separate runs", (1.13, 1.11, 1.15), (1.36, 1.31, 1.41)),
         ("open model, its own earlier note in view", (1.19, 1.11, 1.27), (1.47, 1.26, 1.69)),
         ("top model, its own earlier note in view", (2.60, 2.32, 2.83), (3.65, 3.30, 4.08))]
yy = np.arange(len(right))[::-1]
for yi, (lab, j, t) in zip(yy, right):
    c = GREEN if j[1] > 1.6 else GREY
    axR.errorbar(j[0], yi + 0.14, xerr=[[j[0] - j[1]], [j[2] - j[0]]], fmt="o", color=c, capsize=3, label="word overlap" if yi == yy[0] else None)
    axR.errorbar(t[0], yi - 0.14, xerr=[[t[0] - t[1]], [t[2] - t[0]]], fmt="s", color=c, capsize=3, mfc="white", label="tf-idf cosine" if yi == yy[0] else None)
axR.set_yticks(yy); axR.set_yticklabels([r[0] for r in right], fontsize=8.5)
axR.axvline(1, color="k", lw=0.8); axR.set_xlim(0.8, 4.3); axR.set_ylim(-0.6, len(right) - 0.4)
axR.set_xlabel("how much more alike same-level notes are\nthan different-level notes (ratio, 90%)", fontsize=8.5)
axR.set_title("Does the model carry its note forward?", loc="left", fontsize=9.5)
axR.legend(loc="upper left", fontsize=7.5, frameon=False, bbox_to_anchor=(0.45, 1.0))
if not PAPER: fig.suptitle("Fig. 1  The two gates of note learning: notes move the score only where the writer carries its note", x=0.01, y=1.06, ha="left", fontsize=10)
save(fig, "F1", "F1-notes-at-work")

# ---------------------------------------------------------------- F3 (v9): the budget as a dose-response plot
# Same-day pairs against the base budget (register rows budget-pair-half-sameday, budget-pair-2x, budget-pair-2x-replication, budget-pair):
# x = tokens per game as a multiple of the base budget; y = change in RHAE vs the same-day control; bars = 90% (1.645 s.e.);
# shaded = the acceptance range filed before the run (the 3.7x pair measured the rate first; no band).
pairs = [(0.54, -19.3, 4.5, (-25.0, -8.0), "cut to 0.54×   −19.3"), (1.73, 19.3, 5.4, (8.3, 26.5), "1.7×, first day   +19.3"),
         (1.73, 13.0, 5.2, (8.3, 26.5), "1.7×, second day   +13.0"), (3.68, 35.7, 5.8, None, "3.7×, the first pair   +35.7")]
fig, ax = plt.subplots(figsize=(6.6, 4.0))
for k, (x, d, se, band, lab) in enumerate(pairs):
    xx = x * (1.06 if lab.endswith("second day") else 1.0)
    if band:
        ax.add_patch(plt.Rectangle((xx * 0.90, band[0]), xx * 0.22, band[1] - band[0], color="#e8dcc0", zorder=1))
    ax.errorbar(xx, d, yerr=1.645 * se, fmt="o", color=GREEN if d > 0 else RED, capsize=3, ms=6, zorder=4)
    ax.annotate(lab, (xx, d), xytext=(9, 0), textcoords="offset points", fontsize=7.5, va="center", color="#3f4a45")
ax.axhline(0, color="k", lw=0.8); ax.axvline(1, color=GREY, lw=0.8, ls=":")
ax.text(1.0, 49, "base budget, 158K tokens per game", ha="center", va="top", fontsize=7, color=CAP)
ax.text(0.45, 44, "shaded: acceptance range filed before the run", fontsize=7, color="#8a7d5a", ha="left", va="top")
ax.set_xscale("log"); ax.set_xticks([0.54, 1, 1.73, 3.68]); ax.set_xticklabels(["0.54×", "1×", "1.7×", "3.7×"])
ax.xaxis.set_minor_formatter(plt.NullFormatter()); ax.set_xlim(0.42, 5.2); ax.set_ylim(-32, 50)
ax.set_xlabel("generated tokens per game, as a multiple of the base budget (log)")
ax.set_ylabel("change in RHAE vs the same-day control (90%)")
if not PAPER: ax.set_title("Fig. 2  What converts below the line: thinking time, four same-day pairs", loc="left", pad=16)
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
 ("five more models, all 0", 0, 0, 0),   # rows screen24-*: Luna, Haiku 5.5, Kimi K2, GLM-5.1, Grok Build, 0/23 clean reads
]
fig, ax = plt.subplots(figsize=(7.2, 5.6))
yy = np.arange(len(disc))[::-1]
for yi, (lab, p, lo, hi) in zip(yy, disc):
    c = GREEN if p >= 8 else GREY
    if hi > lo:
        ax.errorbar(p, yi, xerr=[[p - lo], [hi - p]], fmt="o", color=c, capsize=3)
    else:
        ax.scatter(p, yi, color=c, s=40, zorder=5)
    if p >= 8:
        ax.text(hi + 0.4, yi, f"{p:.0f}", fontsize=8.5, va="center", color=GREEN, fontweight="bold")
ax.set_yticks(yy); ax.set_yticklabels([d[0] for d in disc], fontsize=8.5)
for tl, (lab, *_ ) in zip(ax.get_yticklabels(), disc):
    if "ours" in lab: tl.set_fontweight("bold")
ax.axvline(8, color=RED, lw=0.8, ls=":")
ax.text(8.25, len(disc) - 0.45, "bar: 8 of 23", fontsize=8, color=RED)
ax.set_xlim(-0.7, 24.2); ax.set_ylim(-0.7, len(disc) - 0.1)
if PAPER:
    ax.set_xlabel("cells beating nothing-changes (of 23)")
else:
    ax.set_xlabel("cells where the model's program beats the no-change baseline (of 23, 90% interval)")
    ax.set_title("Fig. 3  The gate: who can write a replay-exact simulator of a level", loc="left", pad=16)
ax.text(0.0, -0.155, "* scaled from a 217-cell probe corpus", transform=ax.transAxes, fontsize=7, ha="left", color="#3f4a45")
save(fig, "F4", "F4-discriminator")

# ---------------------------------------------------------------- F4 (v9.1): the loop, minimal research style
# text nodes, no boxes; a return arrow makes it a loop; the two tests hang below as single lines
from matplotlib.patches import FancyArrowPatch
fig, ax = plt.subplots(figsize=(9.6, 2.9)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
INK = "#1a1f1d"; SOFT = "#3f4a45"
def arrow(x0, y0, x1, y1, color="#6b7772", rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=10,
                                 color=color, lw=1.0, connectionstyle=f"arc3,rad={rad}"))
parts = [("writer", "a six-line note\nafter each game"),
         ("selector", "what returns"),
         ("compiler", "the context payload"),
         ("the frozen model", "plays the next game"),
         ("evaluator", "vs a control,\ncriterion filed first")]
xs = [9, 29, 49, 69, 89]
for x, (name, sub) in zip(xs, parts):
    ax.text(x, 66, name, ha="center", va="center", fontsize=10, color=INK, fontweight="bold")
    ax.text(x, 56, sub, ha="center", va="top", fontsize=7.6, color=SOFT, linespacing=1.3)
for a, b in zip(xs[:-1], xs[1:]): arrow(a + 7.5, 66, b - 7.5, 66)
ax.plot([xs[4], xs[4], xs[0]], [71.5, 82, 82], color="#6b7772", lw=1.0)
arrow(xs[0], 82, xs[0], 73.5)
ax.text(50, 85.5, "the read decides what returns", ha="center", va="center", fontsize=7.6, color=SOFT, style="italic")
ax.text(xs[0], 24, "writer test: the same note twice, compared", ha="center", va="center", fontsize=7.6, color=GREEN)
ax.text(xs[3], 24, "certifier: a short probe sorts the model", ha="center", va="center", fontsize=7.6, color=GREEN)
arrow(xs[0], 28, xs[0], 46, GREEN); arrow(xs[3], 28, xs[3], 46, GREEN)
ax.text(50, 6, "fully automatic; every note written at test time, on the game being played; every read pre-registered",
        ha="center", va="center", fontsize=7.6, color=SOFT, style="italic")
if not PAPER: ax.set_title("Fig. 4  The loop: machinery for automated in-context continual learning", loc="left", fontsize=10, pad=16)
save(fig, "F4", "F4-the-loop")

print(f"figures written to {OUT}:", sorted(f for f in os.listdir(OUT) if f.endswith(".png")))
