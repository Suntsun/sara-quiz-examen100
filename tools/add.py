#!/usr/bin/env python3
"""Añade preguntas (JSON en stdin: lista) a data/examen-01.json y valida al momento."""
import json, sys, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent.parent
f = R / "data/examen-01.json"
pool = json.loads(f.read_text()) if f.exists() else []
nuevas = json.load(sys.stdin)
pool += nuevas
f.write_text(json.dumps(pool, ensure_ascii=False, indent=1) + "\n")
print(f"+{len(nuevas)} → {len(pool)} preguntas")
sys.exit(subprocess.call([sys.executable, str(R / "tools/validar_integridad.py")]))
