# Release manifest: the minimum, the recommended, the maximum (composer, 2026-10-28 21:00Z)

Read against the Paper Track rules page (kaggle.com/competitions/arc-prize-2026-paper-track/rules, read 10-28): a valid entry is a Kaggle Writeup (≤ 1,500 words) + a media gallery with a cover image + an attached PUBLIC notebook + an optional public project link (PDF). The winner licence is **CC BY 4.0** on "your winning Submission and the source code used to generate the Submission"; publicly shared competition code is deemed licensed under an OSI-approved licence that does not limit commercial use. Winners must also deliver code capable of generating the winning Submission with a reproduction description. Nothing requires CC0; CC0 was the stale note in the plan and is withdrawn. Final deadline on Kaggle: 9 November 23:59 UTC (we still enter 11-03). Any private Kaggle resource attached to the writeup becomes public after the deadline.

## 1. Minimum (what the rules require)
| item | where | size | licence |
|---|---|---|---|
| Writeup (title, subtitle, body ≤ 1,500 words, references) | Kaggle Writeup, created from draft 6 | 1,497 words | CC BY 4.0 |
| Cover image | runs/paper-figures/v7-draft/cover.png | 1 file | CC BY 4.0 |
| Public notebook | franzen-b1b (the flown kernel: Franzen's M2 cells + our detection/poll cells + the cards patch + the serve values); flip to public at entry | 4.6 MB | MIT (code) |
| Submission ID | draw 1 (30.07) or the best v8 draw by 11-02 | — | — |

That is all the rules ask for. Making the notebook public exposes exactly the kernel: the harness patch and the serve configuration, nothing else.

## 2. Recommended (what the paper's Completeness and Progress claims stand on)
| item | where | size | why |
|---|---|---|---|
| Companion PDF (writeup + long form + Part III + appendices A–H) | runs/paper-companion/companion.pdf, as the Project Link | 1.5 MB | the long form and every appendix the writeup cites |
| Figures F1–F4 + the figure script | runs/paper-figures/v6/ + runs/lib/paper_figures_v6.py | 0.7 MB | reproducible figures |
| Register + pre-registration log | runs/ledger/bets.json, bets.md; PAPER-2026-10-27-PREREG-LOG.md | 0.5 MB | the bar-before-read claim, with the bar text per row |
| Instruments | runs/lib: rhae_pair_read.py, pair_cap_read.py, thinking_signature.py, failure_read.py, wm_replay_probe.py, build_companion.py | 0.3 MB | anyone can re-read a pair or run the probe |
| Harness patches | runs/field/ours/deploy/patches (v41 alloc, v42 provenance, v43 stagger, v44 prose) + the B1b cards patch as applied in the notebook | 0.1 MB | the declared changes, each a diff |
| Probe outputs + the 23-cell transition set | runs/field/ours/probe/*.jsonl (transitions-3.jsonl 503 MB; outputs ≈ 20 MB) | 0.5 GB | the floor screen is re-runnable and re-scorable |
| Per-game benchmark.json of every pair and read | one file per mirror (≈ 100 files, ≈ 40 MB) | 40 MB | every RHAE number re-computable |
| Board forecast file | runs/ledger/board-forecast-2026-10-28.md | — | the pre-registered prediction with its commit |

Shape: a fresh public repository built from a clean tree (git subtree/export of the files above, no history), MIT + CC BY 4.0 as in the arc repo's LICENSE. The arc repository's own history (15 GB, mirrors) is never pushed.

## 3. Maximum (available, not recommended)
Full request traces of every mirror (≈ 100 GB compressed): the model's turn-by-turn transcripts. Released on request to a named reader, not posted. The operator journal (the book, §1–§353, 1.1 MB) and the ops journal: internal; they contain the lab's process, costs, product context and names, and nothing in the paper depends on reading them because the pre-registration log carries each row's bar and read. Plans, directions, STATE, the docs/arc mirror: internal.

## 4. What this protects
Nothing of the lab's product or research programme leaves: the fieldwork repos, the direction documents, the Studio, the detector lane, the lab's positioning. The paper's one claim beyond games is stated in the writeup in one sentence and in the companion's Part III without the programme's text. Attribution is retained (CC BY, MIT), unlike CC0.
