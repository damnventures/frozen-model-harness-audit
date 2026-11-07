#!/bin/bash
# §228a.B.2 — the flown form's harness pointed at a hosted OpenAI-compatible provider (OpenRouter;
# the inference.net deployment if it returns), 25 public games, 1 pass. Env values = the flown
# setup_env byte for byte (as run-endpoint-pair.sh) EXCEPT: provider openrouter (the purpose-built
# provider — streaming, reasoning field, provider ordering, referer headers; NOT openai, which
# normalises to the vllm payload), base URL, model id, key, and ARC3_ASSISTANT_EMPTY_CONTENT=1
# (the empty-assistant-content mitigation; 400 is NOT retried — tool_agent.py:525 — so without this
# flag a provider 400 aborts the turn and discards its tool work).
#   bash runs/field/ours/deploy/run-hosted-pair.sh [GAMES] [RUN_NAME] [MAX_RUNTIME_MIN] [ARM_ENV_FILE]
# ARM_ENV_FILE: optional path to a file of KEY=VAL lines, exported before launch (the arm run's
# switches); omit it for the control run. Secrets are read, never printed.
set -u
ARC=/Users/vanya/work/arc
GAMES=${1:-ar25,bp35,cd82,cn04,dc22,ft09,g50t,ka59,lf52,lp85,ls20,m0r0,r11l,re86,s5i5,sb26,sc25,sk48,sp80,su15,tn36,tr87,tu93,vc33,wa30}
RUN_NAME=${2:-hosted-pair-$(date -u +%Y%m%d-%H%M)}
MAX_RUNTIME_MIN=${3:-60}
ARM_ENV_FILE=${4:-}
MODEL_ID=${MODEL_ID:-qwen/qwen3.8-flash}
export LOCAL_ANALYZER_API_KEY="$(cat $ARC/.secrets/openrouter_key)"
export LOCAL_ANALYZER_BASE_URL=https://openrouter.ai/api/v1
export LOCAL_ANALYZER_PROVIDER=openrouter
export LOCAL_ANALYZER_MODEL_ID="$MODEL_ID"
export ARC3_ASSISTANT_EMPTY_CONTENT=1
export LOCAL_ANALYZER_APP_NAME="ARC3 Agent Harness"
export LOCAL_ANALYZER_ENABLE_THINKING=true
export LOCAL_ANALYZER_TOOL_STEPS=0
export LOCAL_ANALYZER_TOOL_TIMEOUT=30
export LOCAL_ANALYZER_YIELD_SECONDS=0
export LOCAL_ANALYZER_YIELD_TOKENS=2048
export LOCAL_ANALYZER_TEMPERATURE=0.7
export LOCAL_ANALYZER_TOP_P=0.95
export LOCAL_ANALYZER_TOP_K=20
export LOCAL_ANALYZER_CONTEXT_WINDOW=$(( (116+12)*1024 ))
export LOCAL_ANALYZER_MAX_OUTPUT=$(( 12*1024 ))
export LOCAL_ANALYZER_TOOL_OUTPUT_TOKENS=3072
export MULTIMODAL_CONTEXT=current_grid
export MULTIMODAL_UPSCALE=10
export ARC3_PRIORITY_REFRESH_QUEUE=1 ARC3_PRIORITY_PACE=0 ARC3_PRIORITY_TAIL_FADE=1 ARC3_PRIORITY_TAIL_FADE_FRACTION=0.2
export ARC3_PRIORITY_TAIL_LOOKUP=remaining ARC3_PRIORITY_SCORE_NORMALIZATION=1
export ARC3_WARMUP_ACTION_GAMES=1 ARC3_HTTP_RETRY_INITIAL_SECONDS=900 MPLBACKEND=Agg ONLY_RESET_LEVELS=true
export ARC3_CROSS_GAME=${ARC3_CROSS_GAME:-1} ARC3_CROSS_GAME_CARD=${ARC3_CROSS_GAME_CARD:-call}   # B1b, the flown form (§339: an arm env may preset 0 for a cards-off control)
if [ -n "$ARM_ENV_FILE" ]; then
  set -a; . "$ARM_ENV_FILE"; set +a
fi
cd $ARC/runs/field/franzen-milestone2/tree/ARC3-Inference
# re_arc resolves to the local EnvSampler stub; the tufa framework sits beside the tree (as cross_game_e2e.sh).
export PYTHONPATH="$ARC/runs/field/local-reads/stubs:.:../tufa-arc-agi-framework/src:../tufa-arc-agi-framework"
exec $ARC/.venv/bin/python inference/framework/run.py \
  --game "$GAMES" --re-arc-environments-dir $ARC/environment_files \
  --max-runtime-minutes "$MAX_RUNTIME_MIN" --n-passes "${N_PASSES:-1}" --concurrent-jobs "${CONCURRENT:-4}" \
  --model "$MODEL_ID" --run-name "$RUN_NAME" --experiments-dir $ARC/runs/field/local-reads \
  --save-request-logs --deployment-target inline --deployment-wait --max-generated-tokens-per-game ${MAX_GEN_TOKENS:-158000}
