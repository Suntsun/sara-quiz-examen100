#!/usr/bin/env bash
# PostToolUse (Write|Edit): si se ha tocado data/*.json, valida al momento.
# exit 2 devuelve el fallo a Claude para que corrija antes de seguir.
f=$(jq -r '.tool_input.file_path // empty')
[[ "$f" == */sara-quiz-examen100/data/*.json ]] || exit 0
cd "$(dirname "$0")/.." || exit 0
out=$(python3 tools/validar_integridad.py 2>&1) || { echo "$out" >&2; exit 2; }
exit 0
