# v7-draft figure set (2026-10-28)

Script: `paper_figures_v7.py` (run from anywhere; writes PNGs next to itself). House style carried from
v6 (`docs/arc/paper/figures/v6/paper_figures_v6.py`): white bg, font.size 9, top/right spines off,
green `#1f7a4d` / red `#b3382c` / grey `#6b7772`, black zero line, captions under the x-axis, dpi 180.
Register rows are `runs/ledger/bets.json` row numbers; mirrors are `runs/field/pod-mirror/<name>`.
Every PNG was rendered and visually inspected for label overlap/clipping.

- **F1 `F1-adoption-channels.png`** — rows B1b +5.5 [+1.2,+10.1] RHAE (row 18 §362); same-day four-pass replication −0.3 [−4.15, +3.55] (row cards-same-day-pair §364); the two pooled +2.2 [−0.7, +5.1]; A1 +1.2 [−9.2,+11.8] (88); O1 −8 [−24,+7] (60); L1 −9 [−23,+4] (43); B1d −8.6 [−12.6,−4.5] (21); B1c −3.95 [−7.11,−0.53] (20); B1e −4.69 [−7.5,−1.9] (22); P3 −6 ±6, *scaled from 20 games (83); R1 0 [−5,+5] (109); mercury3-cards-25 +0.6 ±1.2 (129, RHAE units, marked †). vs v6: rows grouped by unit with dashed separators and per-group unit labels; A0/split-replication rows dropped; mercury row updated from the 5-game −1 to the 25-game +0.6 ± 1.2 read; P3 plotted unscaled (−6) with the * mark; new title "One channel converts; handed structure does not"; caption no longer clips.
- **F3 `F3-budget-curve.png`** — second same-day pair b1x (159.6K, 33.48) → b2x (316.5K, 52.74), +19.25 ± 5.41, elasticity 0.83 [0.63, 1.01] (row budget-pair-2x §364); cross-day stock points exact from mirrors (median completion tokens/game, mean RHAE): capc 10-21 (158.8K, 39.80; 2026-10-21-capc), ctl 10-25 (158.9K, 33.41; 2026-10-25-rung1ctl), p2c 10-14 (530.9K, 62.81), s7ac 10-15 (502.0K, 62.00), t1c 10-17 (608.3K, 67.78), knoba 10-18 (521.4K, 65.46), knobr 10-18 (456.4K, 64.24); same-day pair budgA (158.7K, 35.72) / budgB (543.0K, 71.46) from 2026-10-28-budgA/-budgB benchmark.json, delta +35.74 ± 5.75 and elasticity 0.53 [0.37, 0.75] from row 122; cross-day log-log fit slope 0.47 recomputed from the mirror points. vs v6: rebuilt — cross-day points now grey/small and exact (v6 rounded), the same-day pair large dark green joined by a thick segment with the elasticity annotation; fit line demoted to light grey background; Kaggle-budget dotted line label moved inside the top-left (no collision); title "The budget curve: one measured slope". Note: row 122's "3.68×" is the ratio of per-game token MEANS (566.4/154.1); the plotted medians give 543.0/158.7 = 3.42.
- **F4 `F4-discriminator.png`** — the replay probe across models: Astra* 174/217 corpus cells scaled ≈ 19 [17, 20] (row 132); GPT-6.1 Terra 20 (screen24-terra); Sol 16 [12, 20] (row 56 §233); MiMo V2.6 Flash 4 [1, 7], DeepSeek V4.1 Flash 3, Nemotron 1, Qwen3.8-27B 0 (row 111); Mercury 3 reasoning off 3 (row 107); Flash-Next 1 (row 56); the 11-04/05 market screen rows (screen24-*).
- **F5 `F5-design-law-map.png`** — schematic. Anchors: open-class probe scores 0–4 of 23 with structure effect ≈ 0; the own-notes point is the pooled null (−0.2 ± 1.3); the above-the-floor own-notes read on Sol (+1.9 ± 6.6, open); frontier band from the published ceiling papers.

## Known discrepancies vs the brief's numbers (register/mirror values used instead)
- F4 MiMo: brief said 3 [1, 5]; register says MiMo 4/23 in three places (rows 111, 121, companion §screen23) and v6 used 4 [1, 7]. Used 4 [1, 7].
- F1 B1d/B1e intervals: brief gave ±~5; used the register's exact [−12.6, −4.5] (21) and [−7.5, −1.9] (22). Both still exclude zero (red), as the brief intended.




## 2026-11-05 revision
- F1: three rows added (MiMo own cards −0.14 ± 2.06; three families pooled same-day −0.33 [−1.7, +1.0]; own notes above the floor on GPT-6.1 Sol, four reads, +1.9 [−8.9, +12.8], open).
- F4: GPT-6.1 Terra 20/23 (row screen24-terra) and the 11-04/05 market screen rows added (Wilson intervals); five unscreenable mid-price models named in the caption, not drawn.
- F5: the own-notes point is the pooled null (−0.2 ± 1.3), grey; the above-the-floor own-notes read (+1.9 ± 6.6, open) added; the text under the left half now reads "nothing delivered converts; thinking time does".
- The figure numbered F2 in earlier drafts is not part of this set.
