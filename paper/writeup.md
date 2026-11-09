# Machinery for Automated In-Context Continual Learning Through Notes: an audit of a frozen model on ARC-AGI-3
*Draft 9 (the lead's final text, 2026-11-09; composer's factual corrections: Agno's lift is on the same game; the note-learning family is automated and trusts a note once written; abstract insight (2) states the writer-test ratio as note consistency, not score improvement). Kaggle Paper Track format, ≤ 1,500 words in the body. Every number traces to a register row (runs/ledger/bets.json) or a figure; bracketed tags map to rows via runs/ledger/tag-map.json.*

## Abstract
We present machinery for automated, in-context, continual learning: a loop that creates, tests and keeps a frozen model's learnings as notes, with no human involved at any step. Systems that learn from their own notes (Reflexion, ExpeL, AutoGuide, ACE) share one assumption: that a written note belongs in the context payload. A learning can overfit, so the loop tests that assumption continually: before a note is trusted, and again as the games change. After each game the model writes a six-line note; a selector filters which notes to retain; a compiler assembles the context payload with the relevant notes; an evaluator measures change to the score. 

We ran it for twelve weeks on Qwen3.8-Flash-Next (125B MoE, W4A16) in the public Duck/Franzen harness, offline on one 96 GB GPU, the Kaggle setting: about twelve thousand notes written and delivered, the loop live on the hidden games. We ran 179 experiments, every read pre-registered and every miss published. Three insights. (1) Some models cannot turn notes into score: below a capability line the model's own notes are delivered and read, yet across three model families they move the score by less than ±1.7 points at 90%. A short probe tells which side of the line a model is on: of more than twenty models screened, nothing under $5 per million output tokens passes; two top models do. (2) Some models cannot write notes that generalise: their notes for one level, written in separate runs, are only 1.1 to 1.4× as alike as their notes for other levels: the note carries the run, not the level. A top model's are 2.6 to 3.7×: it writes the same note again. (3) Below the line, what raises the score is thinking time, not notes: 33 to 53 to 72 of 100 as the token budget rose 1.7× and 3.7×, with diminishing returns, every later read inside a band filed before the run. Above the line the question the loop exists for stays open: a top model reading its own notes moves +1.9 ± 6.6, unresolved.

## 1. The loop, and where it ran (F4)
Structure added to the context uplifts models on ARC-AGI-3 (ARC Prize Foundation, 2026): capability and effort dominate (Rodionov 2026b), and every ceiling result has a model writing a replay-verified executable (Rodionov 2026a; Memento 3, 100 RHAE with a frozen Opus 5; Tycho, Twin, Kepler). Notes from a stronger model carrying a game's mechanics and strategy lift a weaker model on that same game, across models (Agno). The same approach runs outside ARC-AGI-3: Engram (2026) trains a small reader on a stronger writer's fixed notes for knowledge-work lookups — there the reader is trained; here it stays frozen, and guidance must become action. Self-written harnesses gain +2.8, interval through zero (Lehmann and Vahdati 2026).

These processes share the same parts: (1) a writer that turns experience into notes; (2) a selector that filters which notes are worth retaining; (3) a compiler that assembles the context payload with the relevant notes; (4) an evaluator that tests what each learning does. Most trust a note once it is written. Ours measures it: the evaluator reads every change against a control with the criterion filed first, so a note that stops generalising is measured, not believed. Bracketed tags cite rows of the released register.

| | public LB (best entry) | form mean | training |
|---|---|---|---|
| Yi-Chia Chen (top, 43 entries) | 75.56 | undisclosed | undisclosed |
| Franzen | 38.85 | ≈ 26 | none |
| this submission | 30.07 | 27.3 | none flown |

Served W4A16 on one RTX PRO 6000 (10 streams, 158K tokens per game) in Franzen's Milestone 2 Duck, unchanged but for the declared change.

## 2. Do the notes reach the score? (F1)
The model's own notes about games just played, included in the context at the start of play. The first read gave +5.5 ± 2.7 RHAE per 25 games [B1b]. Two pre-registered four-pass replications, notes verified in every arm opener, gave −0.3 ± 2.3 and −2.9 ± 1.8 [cards-same-day, cards-same-day-3]; pooled −0.2 ± 1.3, a gain of +2 excluded. Two further families at the same capability line, MiMo V2.6 Flash and Mercury 3, read the same (−0.1 ± 2.1 and +0.6 ± 1.2 over 25 games) [mimo-cards, mercury3-cards-25]: across three families the effect sits inside ±1.7. The notes do reach behaviour: the first action follows the note on 62% of coin-flip levels against 50.7% and 48.7% controls; they do not convert to score. Everything handed in from outside (a written rulebook, notes from earlier runs, a stronger model's notes) was read and moved nothing (rows O1, B1d, P3).

The writer test explains it. Over 11,087 notes written with no earlier note in view, the open model's notes for one level are 1.1 to 1.4× as alike as its notes for other levels, with or without the writer thinking; with its own earlier note in view (741 notes), 1.2 to 1.5×. GPT-6.1 Sol, re-attempting a game with its first attempt's note in view, writes the same note again: 2.6 to 3.7× (333 notes) [writer-consistency, writer-thinking-consistency]. Below the line the model does not carry even its own note forward; above it, it does.

Above the line the outcome question stays open: Sol re-reading its own notes on second attempts pools +1.9 ± 6.6 [sol-samegame, sol-headroom, sol-rep]. The loop was caught working once, in full: on tn36 Sol cold spent 1,730 actions on level 1 and cleared none of 7; reading its own note from that attempt it cleared 7 of 7. The next day both arms won, so this is the machine working, not the average.

## 3. What converts below the line: thinking time (F2)
Allowed to think longer, the same model scored 33, then 53 (1.7× tokens), then 72 of 100 (3.7×). Elasticity 0.83 [0.63, 1.01] at 1.7× (+19.3 ± 5.4) [budget-2x], replicated on a second day (+13.0 ± 5.2) [budget-2x-rep]; 0.53 [0.37, 0.75] at 3.7× (+35.7 ± 5.8) [budget-pair]; a cut to 0.54× costs −19.3 ± 4.5, elasticity 1.0 [budget-half-sameday]. The first pair measured the rate; three later reads landed inside bands filed before their runs: steep below the base budget, diminishing above. On Mercury 3 and MiMo V2.6 Flash, doubling the budget bought nothing [budget-mercury, mimo-budget]: the law needs a model that converts tokens into levels.

## 4. The gate: the reader's capability (F3)
The replay probe: from 20 shown transitions of a level the model writes a program that predicts the next board, scored on 20 held-out transitions against the nothing-changes baseline; a cell counts when the program beats the baseline by 20 points; the bar is 8 of 23 cells. GPT-6.1 Sol beats it on 16 [12, 20], GPT-6.1 Terra on 20 at half Sol's price [screen24-terra]; the open model on 0 to 1; with reasoning off, seven open models write programs on 18 to 23 cells and generalise on 0 to 4 [screen23]. Of more than twenty models from $0.10 to $10 per million output tokens, nothing under $5 passes. Handing a model the cell's rulebook does not help (1 and 2 beats [R2]): the line is executable-writing. The screen sorts classes, not models within one (MiMo 4 of 23 plays 6 levels, Flash-Next 1 plays 23), and the line replicates on a diffusion architecture (Mercury 3: 3 of 23) [mercury3].

## 5. The evaluator: checking our own measuring
A learning can overfit; so can the audit. Seven capped controls over five days spread sd 2.9 RHAE [day-effect], so every experiment is read against its own control; a four-pass pair reads to ± 2.3 [cards-same-day]. Every experiment is a falsifiable prediction, the criterion filed before the run (Appendix B); misses stay in the register; the three budget bands resolved inside. Leaderboard values are best-of-N (Singh et al., 2025); a private-board forecast is filed before the reveal [board-forecast].

## 6. The flown submission: the loop starts empty on the hidden games
franzen-b1b v1 (30.07): Franzen's Milestone 2 notebook with its loop unchanged (the board rendered as text each turn, the action read from the reply, the oldest messages evicted at the context cap; 110 hidden games under a 9.5-hour wall), plus the model's own notes, written on the hidden games as they are played and compiled into the context at session start and at context drains; no note from any public game is carried in. Serve deltas (+7.85 ± 3.65 on a pod) gave no healthy draw on the box. The last slots flew the stock serve with notes: seven healthy draws, mean 25.7.

## 7. Scope and release
One frozen MoE model, one harness, one benchmark; one to four passes per arm; fourteen draws on the hidden games. Register (179 rows), pre-registration log, patches, instruments, notes corpus, notebook released (MIT, CC BY 4.0).

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
