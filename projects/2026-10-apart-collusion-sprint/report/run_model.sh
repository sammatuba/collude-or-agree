#!/usr/bin/env bash
# Run one OpenRouter model on the held-out split: 6 processes, one per case family, 3 seeds.
# Usage, from lab/:  bash ../projects/2026-10-apart-collusion-sprint/report/run_model.sh <model-id> <logdir> [families]
# Then:  uv run python ../projects/.../report/llm_merge_judge.py merge-model <slug> llm-heldout-<slug>-2026-10-26 <model-id>
set -u
model="$1"; logdir="$2"; fams="${3:-F07 F08 F09 F10 F11 F12}"
slug=$(echo "$model" | sed 's#.*/##; s/[^a-z0-9]/-/g')
mkdir -p "$logdir"
for f in $fams; do
  LLM_ENV_FILE="${LLM_ENV_FILE:-.env.openrouter}" LLM_MODEL="$model" LLM_MAX_TOKENS=1500 \
  nohup uv run python -c "from epistemic_lab.run import main; main(['llm','--split','heldout','--families','$f','--seeds','3','--run-id','part-$slug-$f','--boot','10'])" \
    > "$logdir/$slug-$f.log" 2>&1 &
done
echo "launched $slug: $fams"
