# Improving a Frozen Model's In-Context Learning: No Human, No Overfitting

A loop that tests the note and the reader before trusting either, run pre-registered on ARC-AGI-3. Entry to the ARC Prize 2026 Paper Track (Kaggle), Cultured Computer, November 2026.

Handed structure multiplies a frontier model's ARC-AGI-3 score. This audit asks what it does for a frozen open model (Qwen3.8-Flash-Next, W4A16) offline on one 96 GB GPU, the Kaggle setting, in the public Duck/Franzen harness: 179 pre-registered experiments, each a declared change with its acceptance criterion filed before the run. Below the capability line nothing delivered converts, handed or the model's own notes; what converts is the token budget, at a measured and diminishing rate. The line itself is measured by a one-hour probe that places any model on one side or the other, and the reason the model's own notes do not convert is measurable without ground truth: its notes about one level are barely more alike than its notes about different levels.

## What is here

- `paper/` — the Kaggle writeup (`writeup.md`, the body ≤ 1,500 words), the companion (`companion.pdf`, `companion.md`: the long form, the equivalence study, the lab framing, and appendices A to H including the full register), the figures with their captions and the script that draws them, and the references.
- `register/` — `bets.json`: every pre-registered experiment with its bar, number and read; `prereg-log.md`: which journal section filed and read each row; `board-forecast-2026-10-28.md`: the private-leaderboard forecast filed before the reveal; `tag-map.json`: the writeup's short tags → register ids.
- `instruments/` — the readers: `rhae_pair_read.py` (paired RHAE read over `reads/`), `pair_cap_read.py`, `thinking_signature.py`, `failure_read.py`, `wm_replay_probe.py` (the capability probe), `writer_consistency_read.py` (same-level vs different-level note similarity), the log and companion builders, and the patch tests.
- `patches/` — the declared harness changes as diffs, the hosted-pair launcher, and the arm environment files.
- `probe/` — every replay-probe output, one JSON line per cell. The 23-cell transition set (`transitions-3.jsonl`, 503 MB) is attached to this repository's release as an asset.
- `reads/` — `benchmark.json` of every pod mirror and hosted read: the per-game numbers every pair in the paper is computed from; and `cross_game_cards.jsonl`, the model's own notes per cleared level, where a mirror wrote them.
- `notebook/` — the flown Kaggle kernel (`franzen-b1b-v7.ipynb`) with its metadata.

`DATA.md` describes the layout and what is not released (operator journal, plans, full request traces: about 100 GB, available on request to a named reader).

## Reproduce a number

A pair read: `python3 instruments/rhae_pair_read.py reads/<arm mirror> reads/<control mirror>` prints the paired RHAE difference with its interval. The capability probe: download `transitions-3.jsonl` from the release, then `python3 instruments/wm_replay_probe.py --help`. The writer read: `python3 instruments/writer_consistency_read.py reads/<mirror> [reads/<mirror> ...]` over the `cross_game_cards.jsonl` files released beside each mirror's `benchmark.json` (the open model's notes in the pod mirrors; GPT-6.1 Sol's in the `*sol*` reads); `bash instruments/writer_consistency_paper.sh` prints the paper's two numbers from the exact sets. Every number in the writeup carries a bracketed tag; `register/tag-map.json` maps it to the register row, whose `status` and `read` fields give the bar as filed and the number as read.

## Licence

Code: MIT. Documents, figures and data: CC BY 4.0. See `LICENSE` and `NOTICE`.
