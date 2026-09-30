#!/usr/bin/env bash
# Extrae a texto plano cada PDF de temario/ (misma base de nombre, extensión .txt).
# Los .txt son la ÚNICA fuente contra la que se validan las citas.
set -euo pipefail
cd "$(dirname "$0")/../temario"
shopt -s nullglob
for pdf in *.pdf; do
  pdftotext -enc UTF-8 "$pdf" "${pdf%.pdf}.txt"
  echo "extraído: ${pdf%.pdf}.txt ($(wc -w < "${pdf%.pdf}.txt") palabras)"
done
