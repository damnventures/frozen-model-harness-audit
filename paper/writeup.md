# What a Frozen Model Takes From Its Harness: an audit of in-context learning on ARC-AGI-3
*Draft 7 (composer, 2026-11-08): draft 6's numbers and tags, reframed around the loop; frozen for the entry. Kaggle Paper Track format, ≤ 1,500 words in the body. Every number traces to a register row (runs/ledger/bets.json) or a figure; bracketed tags map to rows via runs/ledger/tag-map.json.*

## Abstract
We present a way to improve a frozen model's in-context learning that needs no human in the loop and cannot overfit. Systems that learn from their own notes (Reflexion, ExpeL, AutoGuide, ACE) assume two things: that the note is worth reading and that the reader can use it. Our loop tests both before anything is trusted. After each game the model writes a six-line note; a selector chooses which notes return; a deliverer places them in the next prompt; a meter reads their effect against a control run the same day, the acceptance criterion filed first; a certifier asks in one hour whether a model can use what it reads; a writer test asks for the same note twice and compares. Every note is written at test time on the game being played, so the loop cannot overfit the public set; every read is pre-registered and every miss published (179 experiments, 158 read), so the audit cannot overfit its result. We ran it for twelve weeks on Qwen3.8-Flash-Next (125B MoE, W4A16) in the public Duck/Franzen harness, offline on one 96 GB GPU, the Kaggle setting. Whether notes reach behaviour is gated by the reader: below the capability line the model's own notes are delivered and read, yet across three families change the score by less than ±1.7 RHAE at 90%; above the line the channel is open (+1.9 ± 6.6, four reads). The reason is measurable without ground truth. The open model's notes for one level, written in separate runs, are 1.1 to 1.4× as alike as its notes for other levels, with or without its writer thinking; a top model's are 2.6 to 3.7×. What converts below the line is the token budget: elasticity 0.83 [0.63, 1.01] at 1.7× tokens and 0.53 [0.37, 0.75] at 3.7×, replicated (+13.0 ± 5.2) and 1.0 on a same-day cut to 0.54× (−19.3 ± 4.5), the three later reads inside bands filed first; on two models that clear one level per game, doubling the budget buys nothing. Notes carried from earlier runs, other games or a stronger model read within ±5 or negative; the flown submission carries none.

## 1. The loop, and where it ran
Handed structure (structure written for the model) multiplies a frontier model's ARC-AGI-3 score: capability and effort dominate (Rodionov 2026b); a stronger writer's manuals transfer within a game (Agno); every ceiling result has a model writing a replay-verified executable (Memento 3 (2026), 100 RHAE with a frozen Opus 5; Tycho, Twin, Kepler). Self-written harnesses gain +2.8 held-out RHAE, interval through zero (Lehmann and Vahdati 2026). Concurrently, Engram (2026) reports a stronger writer's fixed notes helping small readers on knowledge-work lookups, and reinforcement learning on the reader adding more: there notes carry facts to retrieve and the reader is trained; here guidance must become action and the reader stays frozen, so the loop measures whether it can. The loop's parts: a writer (the model's own notes; a guidebook; verified facts), a selector (which notes, how fresh), a deliverer (where, when, in what form), a meter (a 25-game pass at the cap against a same-day control, bar filed first), a certifier (§4), a writer test (§2) and an allocator (§3). Bracketed tags cite rows of the released register.

| | public LB (best entry) | form mean | training |
|---|---|---|---|
| Yi-Chia Chen (top, 43 entries) | 75.56 | undisclosed | undisclosed |
| Franzen | 38.85 | ≈ 26 | none |
| this submission | 30.07 | 27.3 | none flown |

The model is served W4A16 on one RTX PRO 6000 (10 streams, 158K tokens per game) in Franzen's Milestone 2 Duck, unchanged but for the declared change.

## 2. Does the loop reach behaviour? Adoption against outcome (F1)
By delivery channel:

- **The model's own cards about games just played in this run, shown early in the user turn:** +5.5 ± 2.7 RHAE per 25 games, four-pass means against two controls two days earlier [B1b]. Two pre-registered same-day four-pass replications, cards verified in every arm opener: −0.3 ± 2.3, levels identical [cards-same-day], and −2.9 ± 1.8 [cards-same-day-3]. Pooled −0.2 ± 1.3, 90% [−2.3, +1.9]: no effect, +2 excluded. Above the line, Sol re-reading its own notes: on five games it clears, 36 vs 36 levels, −5.9 ± 8.9 [sol-samegame]; on eight hard games, three arms, the pairs are zero (+1.7 ± 19.0; −3.7 ± 10.7) [sol-headroom]; two one-pass movements dissolved on replication (ten runs, all won); above the line pooled +1.9 ± 6.6, unresolved [sol-rep]. A fourth family, MiMo V2.6 Flash: −0.1 ± 2.1 over 25 games [mimo-cards].
- **A harness-written rulebook (Memento 3's language half):** adoption lift 1.54 against an acceptance criterion of 2.0; levels −8 [−24, +7] [O1].
- **Cards from earlier runs:** 218 vs 219 levels [B1d]; bigger blocks −3.95, policy mixes −4.69 [B1c, B1e].
- **Manuals from a stronger player:** other games 149 vs 155, cited in 0 of 1,236 turns [P3]; the same game (Agno's cell), 10 vs 10 [R1].
- **Tools and ledgers:** a verifying tool used 0 of 8,087 calls [simulator-door]; an effect ledger acted on (37%), −9 [−23, +4] [L1].
The writer, measured without ground truth: same-level agreement 1.1 to 1.4× over 11,828 notes, 1.0 to 1.2× with thinking [writer-consistency, writer-thinking-consistency]; Sol 2.6 to 3.7×. The loop delivers and the model reads; below the line, what it reads barely distinguishes one level from another.

## 3. What converts below the line: the budget (F2)
Cutting reasoning length 47% cuts clears 52%, elasticity 1.1 [E1-low]; cutting the token budget to 0.54× on a same-day pair costs −19.3 ± 4.5 RHAE, elasticity 1.0, inside its pre-filed band [budget-half-sameday]. In RHAE, same-day pairs give 0.83 [0.63, 1.01] at 1.7× tokens (+19.3 ± 5.4) [budget-2x], replicated on a second day (+13.0 ± 5.2, 0.48) [budget-2x-rep], and 0.53 [0.37, 0.75] at 3.7× (+35.7 ± 5.8) [budget-pair], the first read; the three later reads landed inside bands filed first: steep below the base budget, diminishing above. On Mercury 3 (27 vs 27 levels) [budget-mercury] and MiMo V2.6 Flash (−1.6 ± 4.2; 40 vs 48 levels) [mimo-budget] 2× tokens bought nothing: the law needs a model that converts tokens into levels.

## 4. The gate: the reader's capability, read in an hour (the floor of F3, F4)
On five games at the same cap Sol clears 31 levels to the open model's 23 on a twentieth of the tokens [teachers]; Astra passes 174 of 217 probe cells [astra-corpus]. On the replay probe (a program from 20 shown transitions scored on 20 held-out against the nothing-changes baseline, criterion 20 points) Sol beats it on 16 of 23 cells [12, 20], the open model on 0 to 1. With reasoning off, seven open models write programs on 18 to 23 cells and generalise on 0 to 4 against the acceptance criterion of 8 [screen23]; handing them the cell's rulebook does not help (1 and 2 beats [R2]); ten samples per step lift Mercury to 8 of 23 at 14× tokens [economy] (10-27; not reproduced 11-06 [mercury-line-bo10-control]). The line is executable-writing, and the screen sorts classes, not models within one (MiMo 4 of 23 plays 6 levels, Flash-Next 1 plays 23); the line replicates on a diffusion architecture (Mercury 3: 3 of 23; 3 levels), where own cards read +0.6 ± 1.2 over 25 games [mercury3, mercury3-cards-25].

## 5. The meter: not overfitting the result (F3)
Seven capped stock controls over five days spread sd 2.9 RHAE [day-effect]: a one-pass pair's s.e. is 5 to 7 RHAE, a four-pass pair's 2.3 [cards-same-day]. Every experiment is a falsifiable prediction: the criterion is filed before the run, which resolves it (Appendix B); the three budget bands resolved inside; misses stay in the register. Leaderboard values are best-of-N (Singh et al., 2025), top-20 public bests 6 to 11 points above form means; a private-board forecast is filed before the reveal [board-forecast].

## 6. The flown submission: nothing carried
franzen-b1b v1 (draw 1, 30.07): Franzen's Milestone 2 notebook with its loop unchanged (the board rendered as text each turn, the action read from the reply, the oldest messages evicted at the context cap; 110 hidden games under a 9.5-hour wall), plus the model's own cards, written on the hidden games as they are played and read at session start and at context drains, and rerun-detection fixes; no note from any public game is carried in. Serve deltas that read +7.85 ± 3.65 on a pod gave no healthy draw in three flights on the box. The last slots fly the stock serve with cards: seven healthy draws, mean 25.7.

## 7. Scope and release
Scope: one frozen MoE model, one harness, one benchmark; one to four passes per arm; 14 hidden draws; the card effect reads as no effect (pooled −0.2 ± 1.3, +2 excluded). Arms that missed their criteria stay in the register with number and criterion. Register (179 rows), pre-registration log, patches, instruments, notes corpus, notebook released (MIT, CC BY 4.0).

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
