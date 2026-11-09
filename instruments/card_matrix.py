#!/usr/bin/env python3
"""The note matrix for the Kaggle card and the cover (§415): real notes from the released corpus, rows = levels of one game,
columns = separate runs; left the open model (tu93), right GPT-6.1 Sol (su15). A card's colour is the hue of its first
content word after GOAL, so cards that say the same thing share a colour. Writes card.png (1120x560) and cover.png (1920x1080)
into runs/paper-figures/v7-draft/. Usage: python3 runs/lib/card_matrix.py [RELEASE_READS_DIR]"""
import sys, os, re, glob, collections, hashlib, textwrap
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from writer_consistency_read import load, words
R = sys.argv[1] if len(sys.argv) > 1 else "/Users/vanya/work/arc/runs/release/2026-11-08/reads"
OUT = "/Users/vanya/work/arc/runs/paper-figures/v7-draft"
BG, MINT, SAGE, INK = "#101a17", "#b9dccb", "#8fbfa8", "#101a17"
PAL = ["#e8c170", "#8fd3c8", "#f2a3a3", "#a9c7f0", "#d9b8f0", "#b7e0a0", "#f0c9a3", "#c9d9f0"]
def goal(r):
    m = re.search(r"GOAL[:\s]*([^\n]*)", r); g = (m.group(1) if m else r.split("\n")[0]).strip()
    return re.split(r"\s(?:CONTROLS|RULE|RULES|HOLDS|NEXT)\b", g)[0].strip().rstrip(".")
def matrix(cards, game, ncol, nrow):
    by = collections.defaultdict(dict)
    for c in sorted(cards, key=lambda c: c["t"]):
        if c["game"] == game and c["src"] not in by[c["level"]]: by[c["level"]][c["src"]] = c
    levels = [l for l in sorted(by) if len(by[l]) >= ncol][:nrow]
    return [[by[l][s] for s in sorted(by[l])[:ncol]] for l in levels], levels
def hue(text):
    w = [x for x in re.findall(r"[a-z]+", text.lower()) if len(x) > 3 and x not in ("reach", "move", "guide", "navigate", "exit", "collect", "using", "while", "from", "with", "into", "onto", "target", "tile", "piece", "token")]
    key = w[0] if w else text[:6]
    return PAL[int(hashlib.md5(key.encode()).hexdigest(), 16) % len(PAL)]
def draw(ax, grid, title, sub, x0, y0, w, h, fs=7.2, cols=None):
    ax.text(x0, y0 + h + 0.025, title, color="white", fontsize=12.5, fontweight="bold", va="bottom")
    ax.text(x0, y0 + h + 0.004, sub, color=MINT, fontsize=8.6, va="bottom")
    nrow, ncol = len(grid), len(grid[0]); gw, gh = w / ncol, h / nrow
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            x, y = x0 + j * gw + 0.006, y0 + h - (i + 1) * gh + 0.008
            g = goal(c["rule"]); col = hue(g)
            ax.add_patch(FancyBboxPatch((x, y), gw - 0.012, gh - 0.016, boxstyle="round,pad=0.004,rounding_size=0.01", fc=col, ec="none", transform=ax.transAxes))
            ax.text(x + 0.008, y + gh - 0.026, "\n".join(textwrap.wrap(" ".join(g.split()[:5]), 16)[:2]), color=INK, fontsize=fs + 1.2, va="top", linespacing=1.15)
    for i, _ in enumerate(grid): ax.text(x0 - 0.006, y0 + h - (i + 0.5) * gh, f"L{i+1}", color=SAGE, fontsize=8.5, ha="right", va="center")
    for j in range(ncol): ax.text(x0 + (j + 0.5) * gw, y0 - 0.012, (cols[j] if cols else f"run {j+1}"), color=SAGE, fontsize=8.5, ha="center", va="top")
def figure(size, with_title):
    openm = [d for d in glob.glob(f"{R}/2026-*") if not re.search(r"sola|solc|cardt|card", d)]
    sol = glob.glob(f"{R}/2026[01]*sol*")
    oc, sc = load(openm), load(sol)
    og, ol = matrix(oc, "tu93", 3, 4); sg, sl = matrix(sc, "su15", 3, 4)
    fig = plt.figure(figsize=size, dpi=100); fig.patch.set_facecolor(BG); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    if with_title:
        ax.text(0.04, 0.94, "Improving a Frozen Model's In-Context Learning: No Human, No Overfitting", color="white", fontsize=27, fontweight="bold", va="top")
        ax.text(0.04, 0.865, "A loop that tests the note and the reader before trusting either, pre-registered on ARC-AGI-3 · 179 experiments · one frozen open model", color=MINT, fontsize=14.5, va="top")
        top, h = 0.70, 0.52; fs = 8.6
    else:
        ax.text(0.04, 0.955, "The writer test: ask for the same note twice, in separate runs, and compare", color="white", fontsize=14, fontweight="bold", va="top")
        top, h = 0.80, 0.60; fs = 7.6
    draw(ax, og, "Open model (Qwen3.8-Flash-Next), game tu93", "the same level, three separate runs: 1.1 to 1.4× as alike as its notes for other levels", 0.075, top - h, 0.40, h, fs, ["run 1", "run 2", "run 3"])
    draw(ax, sg, "Top model (GPT-6.1 Sol), game su15", "a cold attempt, then two second attempts with that note in view: 2.6 to 3.7×", 0.565, top - h, 0.40, h, fs, ["cold", "re-reads its note", "re-reads a rewrite"])
    foot = "Each tile: the first words of a real note's goal line, coloured by its first content word. Below the line the model does not carry even its own note forward; above it, it does."
    ax.text(0.04, 0.035, foot, color=SAGE, fontsize=9.2 if with_title else 8.4, va="bottom")
    return fig
figure((11.2, 5.6), False).savefig(f"{OUT}/card.png", dpi=100, facecolor=BG); plt.close()
figure((19.2, 10.8), True).savefig(f"{OUT}/cover.png", dpi=100, facecolor=BG); plt.close()
print("card.png and cover.png written")
