# What a Frozen Model Takes From Its Harness: an audit of in-context learning on ARC-AGI-3
*Draft 6 (composer, 2026-10-25; current to 2026-10-30). Kaggle Paper Track format, ≤ 1,500 words in the body. Every number traces to a register row (runs/ledger/bets.json), a journal timestamp, or a book section; rows cited inline by short tag; the tag-to-row map is in Appendix A (runs/ledger/tag-map.json). Figures: F1 adoption channels, F2 the budget curve, F3 the floor; F4 (companion) the design-law map. Linked code submission: franzen-b1b (draw 1, 30.07; submission ID in the Writeup). Companion PDF via the Project Link: the long form with the register, the paired-read protocol and standard errors as appendices (bibliography and appendices do not count toward 1,500 words, host-confirmed). Licence: MIT for code, CC BY 4.0 for documents and data (the Paper Track's winner licence).*

## Abstract
Handed structure (structure written for the model) multiplies a frontier model's ARC-AGI-3 score. We ask what it does for a frozen open model offline on one 96 GB GPU, the Kaggle setting. Over twelve weeks we ran a pre-registered audit on Qwen3.8-Flash-Next (125B MoE, W4A16) in the public Duck/Franzen harness: 179 registered experiments, 158 read, each a declared change, acceptance criterion filed first. Below the capability line, nothing delivered converts, handed or the model's own: its own cards (six-line notes after each game) read +5.5 ± 2.7 RHAE (a human baseline on action efficiency) across days, then −0.3 ± 2.3 and −2.9 ± 1.8 in two same-day four-pass replications; pooled with two further families, the effect of a model's own notes is inside ±1.7 at 90%. Cards from earlier runs or a stronger model's read within ±5 or negative; rulebooks are partly adopted; tools go unused. The reason is measurable without ground truth: the open model's notes for one level, written in separate runs, are 1.1 to 1.3× as alike as its notes for other levels, with or without its writer thinking; a top model's are 2.2 to 2.4×. Budget is the lever that converts: elasticity 0.83 [0.63, 1.01] at 1.7× tokens and 0.53 [0.37, 0.75] at 3.7×, replicated (+13.0 ± 5.2) and 1.0 on a same-day cut to 0.54× (−19.3 ± 4.5), the three later reads inside bands filed first; on two models that clear one level per game, doubling the budget buys nothing. Above the line the channel is open (+1.9 ± 6.6, four reads); below it, what converts is budget, and what the model writes does not describe the game.

## 1. Setting and prior work
Rodionov (2026b) shows capability and effort dominate on frontier models. Agno's arcade shows same-game transfer from a stronger writer. Lehmann and Vahdati (2026) find self-written harnesses gain +2.8 held-out RHAE, interval through zero; Lencevicius (2026) recovers 86% of an adapter gap by summarisation. Every ceiling result uses a model writing a replay-verified executable: Memento 3 (2026) compiles a rulebook to code accepted only on exact replay, 100 RHAE with a frozen Opus 5; Tycho, Twin, Kepler likewise; Concurrently, Engram (2026) reports notes from a stronger writer helping small readers on knowledge-work lookups, and reinforcement learning on the reader adding more: there notes carry facts to retrieve; here guidance must become action, and the reader stays frozen. This paper measures the boundary left once those conditions are removed; bracketed tags like [B1b] cite rows of the released register.


| | public LB (best entry) | form mean (expected score of one draw) | training |
|---|---|---|---|
| Yi-Chia Chen (top, 43 entries) | 75.56 | undisclosed | undisclosed |
| Franzen | 38.85 | ≈ 26 | none |
| this submission | 30.07 | 27.3 | none flown |

One frozen model, one harness, one protocol: Qwen3.8-Flash-Next served W4A16 on one RTX PRO 6000 (10 streams stock, 158K tokens per game) in Franzen's Milestone 2 Duck, unchanged but for the declared change. A read is a 25-game pass at the cap against a control; offline, hidden games unseen.

## 2. When is in-context learning adopted? (F1)
By delivery channel:

- **The model's own cards about games just played in this run, shown early in the user turn:** +5.5 ± 2.7 RHAE per 25 games, four-pass means against two controls two days earlier [B1b]; two pre-registered same-day four-pass replications, cards verified in every arm opener: −0.3 ± 2.3, levels identical [cards-same-day], and −2.9 ± 1.8 [cards-same-day-3]; pooled −0.2 ± 1.3, 90% [−2.3, +1.9]: no effect, +2 excluded; the cross-day read sits 2.4 s.e. from the same-day pair. Splits, variants, verification, dose: −1.5 to +3.0 at one pass [A0, cards-family, A1, card-dose]. Above the floor, Sol re-reading its own notes: on five games it clears, 36 vs 36 levels, −5.9 ± 8.9 [sol-samegame]; on eight hard games, three arms, the seven-game pairs are zero (own notes −cold +1.7 ± 19.0; condition-bearing form −3.7 ± 10.7) [sol-headroom]; the two games that moved at one pass were re-run next day, three cold and three noted (tn36), two and two (ls20): all ten won; above the line pooled +1.9 ± 6.6, unresolved [sol-rep]. A fourth family at the floor, MiMo V2.6 Flash: −0.1 ± 2.1 over 25 games, 54 cards delivered [mimo-cards].
- **A harness-written rulebook (Memento 3's language half):** adoption lift 1.54 against an acceptance criterion of 2.0; levels −8 [−24, +7] [O1].
- **Cards from earlier runs:** 218 vs 219 levels [B1d]; bigger blocks −3.95, policy mixes −4.69 [B1c, B1e].
- **Manuals from a stronger player:** other games 149 vs 155, cited in 0 of 1,236 turns [P3]; the same game (Agno's cell), 10 vs 10 [R1].
- **Tools and ledgers:** a verifying tool used 0 of 8,087 calls [simulator-door]; an effect ledger acted on (37%), −9 [−23, +4] [L1].
The same cards labelled as another agent's read +0.9 [s.e. 5.1] [provenance]: no authorship effect. The writer: same-level agreement 1.1 to 1.3× over 11,877 notes, 1.0 to 1.2× with thinking [writer-consistency, writer-thinking-consistency]; Sol 2.2 to 2.4×.

## 3. Where the token budget breaks (F2)
Cutting reasoning length 47% cuts clears 52%, elasticity 1.1 [E1-low]; cutting the token budget to 0.54× on a same-day pair costs −19.3 ± 4.5 RHAE, elasticity 1.0, inside its pre-filed band [budget-half-sameday]. In RHAE, same-day pairs give 0.83 [0.63, 1.01] at 1.7× tokens (+19.3 ± 5.4) [budget-2x], replicated on a second day (+13.0 ± 5.2, 0.48) [budget-2x-rep], and 0.53 [0.37, 0.75] at 3.7× (+35.7 ± 5.8) [budget-pair], which measured the rate first; the three later reads landed inside bands filed before their runs: steep below the base budget, diminishing above. On Mercury 3 (27 vs 27 levels) [budget-mercury] and MiMo V2.6 Flash (−1.6 ± 4.2; 40 vs 48 levels) [mimo-budget] 2× tokens bought nothing: the law needs a model that converts tokens into levels; Liu et al. (2026) report the same shape in Elo per token. By the law, the board's top page (35 to 40) sits 1.5 to 2× tokens per game above our form at the 9-hour wall. Below the floor the one elastic lever is tokens per progressing game; handed structure, the model's own cards and reasoning cuts are inelastic or worse.

## 4. The capability floor is the model's
Same harness, five games, same cap: Sol clears 31 levels to the open model's 23 on a twentieth of the tokens, Astra 37 of 38 [teachers], and 174 of 217 wider probe cells [astra-corpus]; on the replay probe (a program from 20 shown transitions scored on 20 held-out against the nothing-changes baseline, criterion 20 points) Sol beats it on 16 of 23 cells [12, 20], the open model on 0 to 1. With reasoning off, seven open models write programs on 18 to 23 cells and generalise on 0 to 4 against the acceptance criterion of 8 [screen23]; Handing them the cell's rulebook does not help (1 and 2 beats [R2]); ten samples per step lift Mercury to 8 of 23 at 14× tokens [economy] (10-27; not reproduced 11-06 [mercury-line-bo10-control]). The floor is executable-writing; rule inference alone does not clear it; the screen separates classes of models (MiMo 4 of 23 plays 6 levels, Flash-Next 1 plays 23); the floor replicates on a diffusion architecture (Mercury 3: 3 of 23; 3 levels), where own cards read +0.6 ± 1.2 over 25 games [mercury3, mercury3-cards-25].

## 5. The instrument, measured (F3)
Seven capped stock controls over five days spread sd 2.9 RHAE, matching per-game sampling [day-effect]: a one-pass pair's s.e. is 5 to 7 RHAE, a four-pass pair's 2.3 [cards-same-day]; same-day pairing is hygiene. Every experiment is a falsifiable prediction: the criterion is filed before the run, which resolves it (Appendix B); the three budget bands resolved inside. Leaderboard values are best-of-N (Singh et al., 2025): top-20 public bests exceed form means by 6 to 11 points; a private-board forecast is filed before the reveal [board-forecast]. Four of the first seven hidden draws scored 0.00 from a kernel detection defect [draw8, draw9, draw10]; serving is in §6.

## 6. The flown submission
franzen-b1b v1 (draw 1, 30.07): Franzen's Milestone 2 notebook plus the model's own cards at session start and drains, and rerun-detection fixes. Serve deltas that read +7.85 ± 3.65 on a pod pair gave no healthy draw in three flights on the box (14.51 truncated; 0.00, class open; 14.60 at 5.2 of 9.5 h): serving changes did not transfer from pod to box. The last slots fly the stock serve with cards: seven healthy draws, mean 25.7.

## 7. Scope and release
Scope: one frozen MoE model, one harness, one benchmark; one to four passes per arm; 14 hidden draws; the card effect reads as no effect (pooled −0.2 ± 1.3, +2 excluded). Arms that missed their criteria are in the register with number and criterion: card variants, drains, compaction, a reasoning diet, notices, ledgers, effort knobs, serving. Every interval's price is in Appendix G. Register (179 rows), pre-registration log, patches, instruments, notebook released (MIT, CC BY 4.0).

## References (not counted)
- ARC Prize Foundation. ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence. arXiv:2603.24621 (2026). The benchmark and the RHAE score.
- ARC Prize Foundation. Verified results, standard vs provider-adapter harness (X posts and results page, Sep–Oct 2026): GPT-6 Astra 62.7 vs 99.9; GPT-6.1 Sol 52.7 vs 96.4; Gemini 4 Argon 49.8 vs 97.3.
- Rodionov, S. (2026a). Executable World Models for ARC-AGI-3 in the Era of Coding Agents. arXiv:2605.05138. [EWM]
- Rodionov, S. (2026b). Do Coding Agents Need Executable World Models, Simplification, and Verification to Solve ARC-AGI-3? arXiv:2607.15439 (rev. 27 Aug).
- Model cards: Qwen3.8-Flash-Next (Qwen, 2026); Mercury 3 (Inception, 2026); MiMo V2.6 Flash (Xiaomi, 2026); DeepSeek V4.1 Flash (DeepSeek, 2026), all via OpenRouter.
- Zhao, H., Yu, Z., He, Z., Fang, M., Tutunov, R., Bou-Ammar, H., Luo, W., Wang, J. Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks. arXiv:2610.11794 (2026).
- Lehmann, J., Aioanei, A., Vahdati, S. Tycho: Active Abstraction with Programmatic World Models for ARC-AGI-3. arXiv:2607.28287 (2026).
- Skoutnev, A., Acharya, K., Longhitano, G., Udell, M., Ellis, K., Drori, I. Twin: Playing an Unknown Game with a Test-Time Digital Twin. arXiv:2608.14490 (2026).
- Kepler: Auditable World Models for ARC-AGI-3. arXiv:2610.00834 (2026).
- Karten, S., Zhang, A. L., et al. Prime Agent: A Self-Improving RLM Harness. arXiv:2608.23552 (2026).
- Lehmann, J., Vahdati, S. Can LLMs Improve Their Own Harness? A Controlled Study on ARC-AGI-3. arXiv:2610.30499 (2026).
- Agno. arc-agi-arcade. https://github.com/agno-agi/arc-agi-arcade and https://www.agno.com/blog/arc-agi-arcade (2026).
- Tufa Labs. The Duck harness. https://www.tufalabs.ai/research/duck-harness/ and https://github.com/Tufalabs/duck-harness (2026).
- Franzen, D. ARC-AGI-3 Milestone 2: Building on the Duck Harness (write-up and notebook, 2026). The frozen-model baseline this audit runs on.
- Xiong, Z., et al. How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior. ACL 2026 Long. https://aclanthology.org/2026.acl-long.27/
- Liu, K., et al. When Agents Slow Down: Understanding LLM Agents' Test-Time Strategies via Elo-per-token Analysis. arXiv:2609.15309 (2026).
- Wu, C., Passenger, J., Song, Y. Tracing the Thoughts of a Coding Agent Playing ARC-AGI-3: Lessons for Continual Learning. arXiv:2610.11450 (2026).
- Lencevicius, R. When the harness decides success: state that cannot be re-observed. arXiv:2610.26632 (2026).
- Singh, S., et al. The Leaderboard Illusion. arXiv:2504.20879 (2025).
- Engram. Learning in a world of notes (blog post, 4 Nov 2026). https://engram.com/blog/learning-in-a-world-of-notes. Fixed notes written by a stronger model; a small reader (Qwen 3.8 27B, GLM-5.3-Flash) trained by RL with LoRA; no intervals reported.
- cosmorin. Why #1 Is #1 — ARC-AGI-3 Gap Analysis (Kaggle notebook, 2026). The public team whose scheduling defect cost 35 points on the same model class.
