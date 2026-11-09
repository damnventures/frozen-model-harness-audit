#!/usr/bin/env python3
"""The register as squares (Card 1's logic, §417): one square per pre-registered experiment, grouped by what it tested,
coloured by how it resolved. Writes card.png (1120x560, no title) and cover.png (1920x1080, title) into runs/paper-figures/v8/.
Outcome per row: indices 1-142 as curated 2026-10-29 for Card 1 (docs/arc/transport-figures/transport_cards_v4.py);
143-179 curated 2026-11-09 by id below. The lane outside this paper is not drawn (its rows stay in the register)."""
import json, re, sys, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, "/Users/vanya/work/arc/runs/lib"); from update_counts import NOT_RUN
REG = "/Users/vanya/work/arc/runs/ledger/bets.json"; OUT = "/Users/vanya/work/arc/runs/paper-figures/v9"
# the paper's house style (paper_figures_v7/v8): white ground, dark green / dark red / grey, outlines for not run; sans for prose, mono for counts
BG, INK, SOFT, GREEN, RED, GREY, EDGE = "white", "#1a1f1d", "#5d6b64", "#1f7a4d", "#b3382c", "#aab4b1", "#6b7772"
MINT, SAGE, WHITE = INK, SOFT, EDGE
MONO = "DejaVu Sans Mono"
OUTCOME = {"met": {8, 18, 66, 71, 74, 76, 102, 122, 124, 131, 135},
           "missed": {2, 3, 9, 11, 12, 16, 20, 21, 22, 28, 31, 32, 35, 43, 48, 50, 60, 61, 67, 68, 70, 75, 77, 78, 79, 80, 83, 85, 86, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 101, 104, 106, 107, 108, 109, 110, 112, 113, 116, 120, 121, 123, 125, 127, 128, 129, 130, 134},
           "notrun": {6, 13, 23, 26, 30, 36, 40, 46, 51, 52, 57, 58, 72, 73, 98, 100, 114, 118, 119, 136, 140, 141, 142}}
BY_ID = {"cards-above-the-line": "notrun", "budget-pair-half-sameday": "met", "budget-pair-2x-replication": "met", "mimo-budget-pair-2x": "missed",
         "cards-fourth-read-conditional": "notrun", "v82-deltas-plus-detection": "missed", "sol-samegame-own-notes": "missed", "sol-headroom-own-notes": "read",
         "sol-tn36-ls20-replication": "missed", "sol-tn36-coverage-vs-verdict": "notrun", "pod-samegame-own-notes": "notrun", "writer-consistency": "read",
         "writer-thinking-consistency": "met", "mimo-writer-thinking-consistency": "met", "screen24-terra": "met", "terra-play-screen": "notrun",
         "mercury-line-bo10-control": "notrun", "mercury-line-rules-handed": "notrun", "mercury-line-own-rules": "notrun"}
UNSCREENABLE = {"screen24-minimax-m31", "screen24-glm53", "screen24-kimi26", "screen24-mimo25pro", "screen24-step37", "screen24-minimax-m3", "screen24-mistral-large-4", "screen24-kimi-k27-code"}
LANE_RULES = [("training", r"^(T-lane|T1-round1|Sol-mini|null-pipeline|training-mechanism|step0|thinking-collapse|rationaliser|R1-E|laneD|laned-r64|cardfit)"),
              ("budget", r"^(tokens$|E1-low|capc|rhae-budget|budget-pair|B2-reasoning-diet|E1-effort|mimo-budget)"),
              ("serving", r"^(S[1-7]|H8|rung|mamba|serve-|v8-|v82-|allocation|submission-hour|spec-steps|L8-queue|L9-effort|knob-tool|DP-scheduler|S4)"),
              ("floor", r"^(WM|screen2[34]|mercury|mimo-play|Sol-|teacher|TD-screen|open-frontier|astra|sol-timing|mercury-timing|mercury-decide|M1-model-screen|Q1|r1-samegame|r2-rules|terra-play)"),
              ("instrument", r"^(clone$|power$|day-effect|pod-day|cards-family|board-forecast|draw|t1-tool|T1-tool|JV-jev)")]
LANES = [("context", "written for\nthe model to read", 7), ("floor", "which models\ncan use it", 6), ("serving", "how the\nmodel is run", 4), ("budget", "thinking\ntime", 3), ("instrument", "checking our\nown measuring", 3)]
def lane_of(rid):
    for lane, pat in LANE_RULES:
        if re.match(pat, rid): return lane
    return "context"
def classify(i, r):
    if r["id"] in BY_ID: return BY_ID[r["id"]]
    if r["id"].startswith("screen24-"): return "notrun" if r["id"] in UNSCREENABLE else "read"
    if i in OUTCOME["met"]: return "met"
    if i in OUTCOME["missed"]: return "missed"
    if i in OUTCOME["notrun"] or r["id"] in NOT_RUN: return "notrun"
    return "read"
def figure(size, with_title):
    rows = json.load(open(REG))["bets"]
    items = [(lane_of(r["id"]), classify(i, r)) for i, r in enumerate(rows, 1)]
    drawn = [it for it in items if it[0] != "training"]
    tot = {c: sum(1 for it in drawn if it[1] == c) for c in ("met", "missed", "read", "notrun")}
    fig = plt.figure(figsize=size, dpi=100); fig.patch.set_facecolor(BG)
    head = f"Machinery for automated in-context continual learning: {len(items)} pre-registered experiments, {len(drawn)} shown"
    if with_title:
        fig.text(0.06, 0.955, head, color=INK, fontsize=17, ha="left", va="top")
        ax = fig.add_axes([0.06, 0.11, 0.88, 0.72])
    else:
        head = f"Machinery for automated in-context continual learning: {len(items)} pre-registered experiments, {len(drawn)} shown"
        fig.text(0.05, 0.96, head, color=INK, fontsize=10.5, ha="left", va="top")
        ax = fig.add_axes([0.05, 0.14, 0.90, 0.72])
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    colors = {"met": GREEN, "missed": RED, "read": GREY, "notrun": "white"}
    units = sum(l[2] for l in LANES); lane_gap = 3.0
    pitch = (100 - lane_gap * (len(LANES) - 1)) / units; tile = pitch * 0.78
    maxrows = max(-(-sum(1 for it in drawn if it[0] == ln) // per) for ln, _, per in LANES)
    ax_w, ax_h = (0.88 * size[0], 0.70 * size[1]) if with_title else (0.90 * size[0], 0.74 * size[1])
    rowh = min(80.0 / maxrows, pitch * (ax_w / ax_h)); tileh = rowh * 0.78
    x, y_top = 0.0, 81.0
    for ln, label, per_row in LANES:
        its = [it for it in drawn if it[0] == ln]; width = per_row * pitch
        won = sum(1 for it in its if it[1] == "met")
        ax.text(x + width / 2, 100, label, ha="center", va="top", fontsize=10.5 if with_title else 9, color=INK, linespacing=1.2)
        ax.text(x + width / 2, 87.5, f"n={len(its)}  met={won}", ha="center", va="top", fontsize=9 if with_title else 8, color=SOFT, family=MONO)
        for k, (_, cls) in enumerate(its):
            cx = x + (k % per_row) * pitch; cy = y_top - (k // per_row) * rowh - tileh
            ax.add_patch(Rectangle((cx, cy), tile, tileh, fc=colors[cls], ec=EDGE if cls == "notrun" else "white", lw=0.8 if cls == "notrun" else 0.5, zorder=3))
        x += width + lane_gap
    y = 0.06 if with_title else 0.07; fs = 12 if with_title else 10.5
    parts = [("met", GREEN, f"criterion met  {tot['met']}"), ("missed", RED, f"criterion missed  {tot['missed']}"), ("read", GREY, f"measured, no criterion  {tot['read']}"), ("notrun", "white", f"filed, not run  {tot['notrun']}")]
    xpos = 0.06 if with_title else 0.05
    for cls, col, txt in parts:
        fig.patches.append(Rectangle((xpos, y), 0.012, 0.012 * size[0] / size[1], transform=fig.transFigure, fc=col, ec=EDGE if cls == "notrun" else col, lw=0.8, figure=fig))
        fig.text(xpos + 0.018, y, txt, color=SOFT, fontsize=fs - 1, ha="left", va="bottom", family=MONO); xpos += 0.215 if with_title else 0.235
    return fig, tot, len(drawn)
fig, tot, n = figure((11.2, 5.6), False); fig.savefig(f"{OUT}/card.png", dpi=100, facecolor=BG); plt.close(fig)
fig, tot, n = figure((19.2, 10.8), True); fig.savefig(f"{OUT}/cover.png", dpi=100, facecolor=BG); plt.close(fig)
print("drawn", n, tot)
