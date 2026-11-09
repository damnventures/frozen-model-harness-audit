*v8 (2026-11-09): the v7 figures with one-line titles and short labels; the provenance and footnotes that were drawn under the axes in v7 are kept here. Fig. 1 = F1, Fig. 2 = F3, Fig. 3 = F4, Fig. 4 = F5. The cover and the card are the register as squares (runs/lib/card_squares.py): one square per pre-registered experiment, grouped by what it tested and coloured by how it resolved (green met, red against, grey measured without a prediction, outlined not run); 162 of the 179 rows are drawn, the rest belong to a lane outside this paper. Outcomes per row: indices 1 to 142 as curated 2026-10-29, the later rows curated 2026-11-09 in the script.*

# Caption library (companion PDF), Memento 3 conventions

Conventions follow Memento 3 (arXiv 2610.11794): no title inside the figure; the caption's first
sentence is the title; captions are self-contained (what each element shows, what every color and
symbol means, interval/unit semantics, data provenance); in-text references use the figure as a
sentence subject ("Figure 2 summarises…", "Figure 5 shows…").

Numbering note: the Kaggle writeup (markdown, which has no caption support) keeps its existing
F1–F3 inline tags and the titled PNGs in this directory. The numbering below applies to the
companion PDF, whose figures are the untitled renders in `paper/` (file tags F5, F1, F3, F4 for Figures 1 to 4)
(`python3 paper_figures_v7.py --paper`). Register rows are `runs/ledger/bets.json` row numbers;
mirrors are `runs/field/pod-mirror/<name>`.

## Figures

**Figure 1: The design-law map: where structure is used and where it is not.** A schematic anchored
on measured points. The x-axis is a model's score on the one-hour replay probe: of 23 (game, level)
cells, the number on which the model's written simulator beats a nothing-changes baseline by at
least 20 points on held-out transitions. The y-axis is what harness structure does: below the floor
it is the measured paired structure effect on the frozen open model; above the floor it is the RHAE
the ceiling papers reach with structure. Grey points left: the open class (probe 0 to 4 of 23) with
structure effects consistent with zero; the larger grey point is the model's own notes, pooled over
three four-pass reads (−0.2 ± 1.3; within ±1.7 over three families). Grey diamond right: the same
channel above the floor on GPT-6.1 Sol, four reads pooled, +1.9 ± 6.6, open. Grey points top right:
Memento 3 at 100 RHAE and Tycho, Twin and Kepler in the 93 to 100 band, from the published ceiling
papers. The dashed vertical line is the floor. The figure is a schematic; the measured points are
the probe scores and the structure effects. The takeaway: below the floor nothing delivered
converts and thinking time does; above it structure is used in the published systems, and our own
read of the notes channel there is open.

**Figure 2: Nothing delivered converts; the model's own notes close at zero.** Each row is one
pre-registered adoption channel, plotted as the paired effect against its control with its 90%
interval; rows are grouped by unit (top: RHAE; middle: levels per 25 games; bottom: levels per 5
games). Green marks an interval entirely above zero, red entirely below, grey covering zero. Top
group: the model's own notes, first read across days +5.5 [+1.2, +10.1]; two same-day four-pass
replications −0.3 and −2.9; the three pooled −0.2 [−2.3, +1.9]; a second family (MiMo V2.6 Flash)
−0.1; three families pooled from same-day reads −0.3 [−1.7, +1.0]; and the same channel above the
floor (GPT-6.1 Sol, four reads) +1.9 [−8.9, +12.8], open. Middle group: verified own notes, a
harness-written rulebook, an effect ledger with enforced expectation, notes from an earlier run,
bigger ordered blocks, policy mixes, manuals about other games (marked *, scaled from 20 games).
Bottom group: a manual about the very game from a stronger writer, and Mercury 3's own notes
(marked †, RHAE units). All values are register rows. The takeaway: the one positive read was
across days; on the same day, and across three families, the effect of a model's own notes is
inside ±1.7.

**Figure 3: The budget curve: a measured rate, diminishing.** Public RHAE (25 games) against
generated tokens per game (log-log). Small grey points are cross-day stock reads from their pod
mirrors; the dashed grey line is their log-log fit. The green points joined by thick segments are
same-day pairs: 3.7× tokens, 35.7 to 71.5 RHAE, elasticity 0.53 [0.37, 0.75] (register row
budget-pair), and 1.7× tokens, +19.3 ± 5.4, elasticity 0.83 [0.63, 1.01] (budget-pair-2x), the
latter replicated on a second day. The red dotted line marks the Kaggle budget, 158K tokens per
game. The takeaway: below the floor, tokens per progressing game are the elastic lever, steep
near the base budget and diminishing above it.

**Figure 4: The floor, measured: who can write a replay-exact simulator.** Each row is one model
on the 23-cell replay probe: the number of cells on which the model's written program beats a
nothing-changes baseline by at least 20 points on 20 held-out transitions. Green marks models
above the pre-registered bar of 8 of 23 (red dotted line), grey those below. Above: GPT-6 Astra
(scaled from the 217-cell corpus), GPT-6.1 Terra 20, GPT-6.1 Sol 16. Below: every open model and
every other model screened from $0.10 to $5 per million output tokens, at 0 to 4 cells. Intervals
are 90% (bootstrap for the earlier rows, Wilson for the rows of 4 to 5 November). Six mid-price
models whose reasoning is mandatory and unbounded could not be measured at a fixed cap and are not
drawn; two more (Kimi K2.6, MiMo V2.5 Pro) were stopped for cost after 6 and 7 cells with none
passing, which is not a read against a bar of 8, and are not drawn either. The screen costs under $10 and about one hour per model. The takeaway: on this probe
capability arrives with price; nothing under $5 per million output crossed the bar.

## Tables

**Table 1: Public leaderboard best entry, per-draw form mean, and training status for the top
entry, the Franzen baseline this audit builds on, and this submission.** "Public LB (best entry)"
is the team's best public leaderboard score, a best-of-N over that team's entries (Yi-Chia Chen,
43 entries: 75.56); "form mean per draw" is the expected score of one draw of the same system
(Franzen ≈ 26 against a public best of 38.85; this submission 27.3 against 30.07), and "training"
records whether the flown entry carries trained weights (none, in both harness entries; undisclosed
for the top entry). Public bests are best-of-N over each team's entries; form means are per-draw.
Leaderboard values from the public ARC-AGI-3 leaderboard; the Franzen form mean and this
submission's draws from the campaign register (hidden draws; register rows tagged board-forecast,
draw8, draw9). The takeaway: the submission is the audit's instrument, not a bid — best-of-N
lifts the board above any system's form.

**Table 2: The register of pre-registered bets (179 rows at this revision).** One row per bet. "id" is the bet's
running number and short tag; "status" is its disposition at the freeze (passed / missed / null /
closed / held / void, as filed); "number" is the measured read with its interval where one was
filed (levels per 25 games or RHAE, paired against the bet's pre-registered control); "read" is
the one-line statement of what the read established; "where" cites the book section (§) or journal
timestamp of the full record. Every bar was filed before its run launched; the pre-registration
log is the companion's Appendix B. Source: the campaign register, runs/ledger/bets.json. The
takeaway: every claim in the paper traces to a row whose bar predates its data.
