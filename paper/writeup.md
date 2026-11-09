# What a Frozen Model Takes From Its Harness: an audit of in-context learning on ARC-AGI-3
*Draft 8 (composer, 2026-11-08): draft 7 curated to the numbers that carry the claim; the rest of the register is in the companion. Kaggle Paper Track format, ≤ 1,500 words in the body. Every number traces to a register row (runs/ledger/bets.json) or a figure; bracketed tags map to rows via runs/ledger/tag-map.json.*

## Abstract
We present a way to improve a frozen model's in-context learning that needs no human in the loop and cannot overfit. Systems that learn from their own notes (Reflexion, ExpeL, AutoGuide, ACE) assume two things: that the note is worth reading and that the reader can use it. Our loop tests both before anything is trusted. After each game the model writes a six-line note; a selector chooses which notes return; a deliverer places them in the next prompt; a meter reads their effect against a control run the same day, the acceptance criterion filed first; a certifier asks in one hour whether a model can use what it reads; a writer test asks for the same note twice and compares. Every note is written at test time on the game being played, so the loop cannot overfit the public set; every read is pre-registered and every miss published (179 experiments, 158 read), so the audit cannot overfit its result. We ran it for twelve weeks on Qwen3.8-Flash-Next (125B MoE, W4A16) in the public Duck/Franzen harness, offline on one 96 GB GPU, the Kaggle setting: about twelve thousand notes written and delivered, fourteen hidden draws flown with the loop live. Three results. The certifier sorts the market: more than twenty models screened in an hour each, nothing under $5 per million output tokens passes, two top models do. Below that line the model's own notes are delivered and read, yet across three families change the score by less than ±1.7 RHAE at 90%, and the writer test says why: the open model's notes for one level, written in separate runs, are 1.1 to 1.4× as alike as its notes for other levels; a top model's are 2.6 to 3.7×. The lever the loop priced more than doubled the model's score toward a person's, 33 to 53 to 72 of 100 as thinking time rose 1.7× and 3.7×, every later read inside a band written before the run. Where a top model reads its own notes the channel is open (+1.9 ± 6.6).

## 1. The loop, and where it ran
Handed structure (structure written for the model) multiplies a frontier model's ARC-AGI-3 score (ARC Prize Foundation, 2026): capability and effort dominate (Rodionov 2026b); a stronger writer's manuals transfer within a game (Agno); every ceiling result has a model writing a replay-verified executable (Rodionov 2026a; Memento 3 (2026), 100 RHAE with a frozen Opus 5; Tycho, Twin, Kepler); self-written harnesses gain +2.8, interval through zero (Lehmann and Vahdati 2026). Concurrently, Engram (2026) trains a small reader to use a stronger writer's fixed notes on knowledge-work lookups: there notes carry facts to retrieve and the reader is trained; here guidance must become action and the reader stays frozen. The loop's parts: a writer (the model's own notes; a guidebook; verified facts), a selector (which notes, how fresh), a deliverer (where, when, in what form), a meter (a 25-game pass at the cap against a same-day control, bar filed first), a certifier (§4), a writer test (§2) and an allocator (§3). Bracketed tags cite rows of the released register.

| | public LB (best entry) | form mean | training |
|---|---|---|---|
| Yi-Chia Chen (top, 43 entries) | 75.56 | undisclosed | undisclosed |
| Franzen | 38.85 | ≈ 26 | none |
| this submission | 30.07 | 27.3 | none flown |

Served W4A16 on one RTX PRO 6000 (10 streams, 158K tokens per game) in Franzen's Milestone 2 Duck, unchanged but for the declared change.

## 2. Does the loop reach behaviour? (F1)
The model's own notes about games just played, shown early in the user turn, read +5.5 ± 2.7 RHAE per 25 games against two controls two days earlier [B1b]. Two pre-registered same-day four-pass replications, cards verified in every arm opener, read −0.3 ± 2.3 and −2.9 ± 1.8 [cards-same-day, cards-same-day-3]; pooled −0.2 ± 1.3, a gain of +2 excluded. Two further families at the line, MiMo V2.6 Flash and Mercury 3, read the same (−0.1 ± 2.1 and +0.6 ± 1.2 over 25 games) [mimo-cards, mercury3-cards-25]: across three families the effect is inside ±1.7. Everything handed from outside was read and moved nothing: a harness-written rulebook partly adopted, notes from earlier runs, a stronger model's manuals, a verifying tool, a ledger of effects (F1; rows O1, B1d, P3, L1 and others in the register). The writer test says why. Over 11,828 notes, the open model's notes for one level, written in separate runs, are 1.1 to 1.4× as alike as its notes for other levels, with or without its writer thinking; GPT-6.1 Sol's are 2.6 to 3.7× [writer-consistency, writer-thinking-consistency]. Below the line the loop delivers and the model reads, but what it reads barely distinguishes one level from another.

Above the line, Sol re-reading its own notes on a second attempt: five games it clears anyway, no lift; eight hard games, three arms, the pairs at zero; pooled +1.9 ± 6.6, open [sol-samegame, sol-headroom, sol-rep]. The loop caught working, one pass: on tn36 Sol cold spent 1,730 actions on level 1 and cleared none of 7; reading its own note from that attempt it cleared 7 of 7; the next day both arms won, so this is the machine working, not the average.

## 3. What converts below the line: the budget (F2)
Allowed to think longer, the same model scored 33, then 53 (1.7× tokens), then 72 of 100 (3.7×). Same-day pairs give elasticity 0.83 [0.63, 1.01] at 1.7× (+19.3 ± 5.4) [budget-2x], replicated on a second day (+13.0 ± 5.2) [budget-2x-rep], and 0.53 [0.37, 0.75] at 3.7× (+35.7 ± 5.8) [budget-pair]; a same-day cut to 0.54× costs −19.3 ± 4.5, elasticity 1.0 [budget-half-sameday]. The first pair measured the rate; the three later reads landed inside bands filed before their runs: steep below the base budget, diminishing above. On two models that clear about one level per game, Mercury 3 and MiMo V2.6 Flash, doubling the budget bought nothing [budget-mercury, mimo-budget]: the law needs a model that converts tokens into levels.

## 4. The gate: the reader's capability, read in an hour (F3)
The replay probe: from 20 shown transitions of a level the model writes a program that predicts the next board, scored on 20 held-out transitions against the nothing-changes baseline; a cell counts when the program beats the baseline by 20 points; the bar is 8 of 23 cells. GPT-6.1 Sol beats it on 16 [12, 20], GPT-6.1 Terra on 20 at half Sol's price [screen24-terra]; the open model on 0 to 1; with reasoning off, seven open models write programs on 18 to 23 cells and generalise on 0 to 4 [screen23]. Across more than twenty models from $0.10 to $10 per million output tokens nothing under $5 passes, and the screen costs under $10 and one hour per model. Handing a model the cell's rulebook does not help (1 and 2 beats [R2]): the line is executable-writing, and the screen sorts classes, not models within one (MiMo 4 of 23 plays 6 levels, Flash-Next 1 plays 23). The line replicates on a diffusion architecture (Mercury 3: 3 of 23) [mercury3].

## 5. The meter: not overfitting the result
Seven capped stock controls over five days spread sd 2.9 RHAE [day-effect], so every pair is read against a control run the same day; a four-pass pair reads to ± 2.3 [cards-same-day]. Every experiment is a falsifiable prediction: the criterion is filed before the run (Appendix B), misses stay in the register, and the three budget bands resolved inside. Leaderboard values are best-of-N (Singh et al., 2025); a private-board forecast is filed before the reveal [board-forecast].

## 6. The flown submission: nothing carried
franzen-b1b v1 (draw 1, 30.07): Franzen's Milestone 2 notebook with its loop unchanged (the board rendered as text each turn, the action read from the reply, the oldest messages evicted at the context cap; 110 hidden games under a 9.5-hour wall), plus the model's own cards, written on the hidden games as they are played and read at session start and at context drains; no note from any public game is carried in. Serve deltas (+7.85 ± 3.65 on a pod) gave no healthy draw on the box. The last slots fly the stock serve with cards: seven healthy draws, mean 25.7.

## 7. Scope and release
One frozen MoE model, one harness, one benchmark; one to four passes per arm; 14 hidden draws. Register (179 rows), pre-registration log, patches, instruments, notes corpus, notebook released (MIT, CC BY 4.0).

## References (not counted)
- Shinn, N., et al. Reflexion: Language Agents with Verbal Reinforcement Learning. arXiv:2303.11366 (2023).
- Zhao, A., et al. ExpeL: LLM Agents Are Experiential Learners. arXiv:2308.10144 (2023).
- Fu, Y., et al. AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents. arXiv:2403.08978 (2024).
- Zhang, Q., et al. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. arXiv:2510.04618 (2025).
- ARC Prize Foundation. ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence. arXiv:2603.24621 (2026). The benchmark and the RHAE score.
- ARC Prize Foundation. Verified results, standard vs provider-adapter harness (X posts and results page, Sep–Oct 2026): GPT-6 Astra 62.7 vs 99.9; GPT-6.1 Sol 52.7 vs 96.4; Gemini 4 Argon 49.8 vs 97.3.
- Rodionov, S. (2026a). Executable World Models for ARC-AGI-3 in the Era of Coding Agents. arXiv:2605.05138. [EWM]
- Rodionov, S. (2026b). Do Coding Agents Need Executable World Models, Simplification, and Verification to Solve ARC-AGI-3? arXiv:2607.15439 (rev. 27 Aug).
- Model cards: Qwen3.8-Flash-Next (Qwen, 2026); Mercury 3 (Inception, 2026); MiMo V2.6 Flash (Xiaomi, 2026); DeepSeek V4.1 Flash (DeepSeek, 2026), all via OpenRouter.
- Zhao, H., Yu, Z., He, Z., Fang, M., Tutunov, R., Bou-Ammar, H., Luo, W., Wang, J. Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks. arXiv:2610.11794 (2026).
- Lehmann, J., Aioanei, A., Vahdati, S. Tycho: Active Abstraction with Programmatic World Models for ARC-AGI-3. arXiv:2607.28287 (2026).
- Skoutnev, A., Acharya, K., Longhitano, G., Udell, M., Ellis, K., Drori, I. Twin: Playing an Unknown Game with a Test-Time Digital Twin. arXiv:2608.14490 (2026).
- Kepler: Auditable World Models for ARC-AGI-3. arXiv:2610.00834 (2026).
- Lehmann, J., Vahdati, S. Can LLMs Improve Their Own Harness? A Controlled Study on ARC-AGI-3. arXiv:2610.30499 (2026).
- Agno. arc-agi-arcade. https://github.com/agno-agi/arc-agi-arcade and https://www.agno.com/blog/arc-agi-arcade (2026).
- Tufa Labs. The Duck harness. https://www.tufalabs.ai/research/duck-harness/ and https://github.com/Tufalabs/duck-harness (2026).
- Franzen, D. ARC-AGI-3 Milestone 2: Building on the Duck Harness (write-up and notebook, 2026). The frozen-model baseline this audit runs on.
- Singh, S., et al. The Leaderboard Illusion. arXiv:2504.20879 (2025).
- Engram. Learning in a world of notes (blog post, 4 Nov 2026). https://engram.com/blog/learning-in-a-world-of-notes. Fixed notes written by a stronger model; a small reader (Qwen 3.8 27B, GLM-5.3-Flash) trained by RL with LoRA; no intervals reported.
