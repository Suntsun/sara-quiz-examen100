#!/usr/bin/env bash
# Extrae a texto plano cada PDF de temario/ (recursivo): junto a cada PDF, mismo nombre + .txt
# Los .txt son la ÚNICA fuente contra la que se validan las citas.
set -euo pipefail
cd "$(dirname "$0")/../temario"
find . -type f -iname '*.pdf' -print0 | while IFS= read -r -d '' pdf; do
  txt="${pdf%.*}.txt"
  pdftotext -enc UTF-8 "$pdf" "$txt"
  printf '%6d palabras  %s\n' "$(wc -w < "$txt")" "${txt#./}"
done
