#!/usr/bin/env bash
# The paper's two writer-consistency numbers from the released tree (run from the release root).
# Open model: every pod mirror's notes except the student arms (sola, solc) and the thinking-on arms (cardt1, cardt2; their own row).
# Sol: the seven hosted GPT-6.1 Sol reads. Same instrument, same filter (a note must carry GOAL; excerpt fallbacks excluded).
set -euo pipefail
cd "$(dirname "$0")/.."
OPEN=$(for d in reads/2026-*/; do [ -f "$d/cross_game_cards.jsonl" ] && echo "${d%/}"; done | grep -v 'sola\|solc\|cardt')
SOL=$(for d in reads/2026[01]*sol*/; do [ -f "$d/cross_game_cards.jsonl" ] && echo "${d%/}"; done)
echo "== Qwen3.8-Flash-Next (pod mirrors)"; python3 instruments/writer_consistency_read.py $OPEN --boot 500 --seed 1 | grep ratio
echo "== GPT-6.1 Sol (hosted reads)";       python3 instruments/writer_consistency_read.py $SOL  --boot 500 --seed 1 | grep ratio
