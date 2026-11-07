# Data

Assembled 2026-11-07 by runs/lib/build_release.py from the campaign tree (no history).

- paper/: the writeup, the companion (PDF + markdown), references, figures and the figure script's output.
- register/: bets.json (every pre-registered experiment with its bar, number and read), the pre-registration log, the private-board forecast filed before the reveal.
- instruments/: the readers (RHAE paired read, capped pair read, thinking signature, failure anatomy), the replay probe, the figure, log and companion builders, and the patch fixtures.
- patches/: the declared changes as diffs (v41 allocation, v42 provenance, v43 stagger, v44 prose) plus the hosted-pair launcher and arm env files.
- probe/: every replay-probe output (per cell: program, shown/held-out exactness, baselines, tokens, timing).
- notebook/: the flown kernel source (franzen-b1b v7) with its Kaggle metadata.
- reads/: benchmark.json of every pod mirror (110 runs) and every hosted read; the per-game RHAE every pair number is computed from.

Files above GitHub's size limit are not in this tree and are published as release assets:
- runs/field/ours/probe/transitions-3.jsonl (503 MB)

Not released: the operator journal, plans, internal records and the mirrors' full request traces (≈ 100 GB; available on request to a named reader).
