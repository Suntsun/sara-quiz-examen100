#!/usr/bin/env python3
"""
validar_integridad.py — Guardián de integridad del temario.

REGLA DURA: toda pregunta se basa única y exclusivamente en el temario
entregado. Cada pregunta lleva una cita literal (`fuente.cita`) que debe
existir tal cual en el texto extraído del documento fuente (`temario/*.txt`).
Si la cita no aparece, la pregunta no entra.

Bloquea (exit 1):
  - temario/ sin textos extraídos (no se puede verificar = no se acepta)
  - esquema inválido (id, pregunta, opciones 3-4 únicas, correcta en rango)
  - falta fuente.documento o fuente.cita, o la cita tiene < 25 caracteres
  - la cita no aparece literal en el documento indicado
  - ids o enunciados duplicados entre todos los quizzes
Avisa (no bloquea):
  - un quiz no tiene exactamente 100 preguntas
  - la respuesta correcta comparte poco vocabulario con la cita (revisión manual)

Uso: python3 tools/validar_integridad.py [--quiet]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
TEMARIO = RAIZ / "temario"
MANIFEST = DATA / "quizzes-manifest.json"
PREGUNTAS_POR_EXAMEN = 100
MIN_CITA = 25
UMBRAL_SOLAPE = 0.5


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFC", texto)
    t = t.replace("­", "")                     # guion blando
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)     # palabra partida a final de línea
    t = t.translate(str.maketrans({"“": '"', "”": '"', "«": '"', "»": '"',
                                   "‘": "'", "’": "'", "–": "-", "—": "-"}))
    return re.sub(r"\s+", " ", t).strip()


def palabras(texto: str) -> set:
    return {w for w in re.findall(r"\w+", normalizar(texto).lower()) if len(w) > 4}


def main() -> int:
    quiet = "--quiet" in sys.argv
    errores, avisos = [], []

    textos = {p.name: normalizar(p.read_text(encoding="utf-8"))
              for p in sorted(TEMARIO.glob("*.txt"))}

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[BLOQUEO] manifest ilegible: {e}")
        return 1

    if manifest and not textos:
        print("[BLOQUEO] temario/ no contiene textos extraídos (.txt). "
              "Sin fuente no hay verificación posible: ninguna pregunta entra.")
        return 1

    ids, enunciados, total = {}, {}, 0
    for entrada in manifest:
        ruta = RAIZ / entrada.get("archivo", "")
        if not ruta.is_file():
            errores.append(f"{entrada.get('id')}: archivo inexistente {ruta.name}")
            continue
        try:
            pool = json.loads(ruta.read_text(encoding="utf-8"))
        except Exception as e:
            errores.append(f"{ruta.name}: JSON inválido ({e})")
            continue
        if len(pool) != PREGUNTAS_POR_EXAMEN:
            avisos.append(f"{ruta.name}: {len(pool)} preguntas (objetivo {PREGUNTAS_POR_EXAMEN})")

        for i, q in enumerate(pool):
            total += 1
            qid = q.get("id") or f"{ruta.name}#{i}"
            tag = f"{ruta.name}:{qid}"
            if not q.get("id"):
                errores.append(f"{tag}: falta id")
            elif qid in ids:
                errores.append(f"{tag}: id duplicado (también en {ids[qid]})")
            else:
                ids[qid] = ruta.name

            enun = normalizar(q.get("pregunta", "")).lower()
            if not enun:
                errores.append(f"{tag}: pregunta vacía")
            elif enun in enunciados:
                errores.append(f"{tag}: enunciado duplicado (también en {enunciados[enun]})")
            else:
                enunciados[enun] = tag

            ops = q.get("opciones")
            if not isinstance(ops, list) or len(ops) not in (3, 4) \
                    or any(not str(o).strip() for o in ops):
                errores.append(f"{tag}: opciones deben ser 3 o 4 textos no vacíos")
                continue
            if len({normalizar(o).lower() for o in ops}) != len(ops):
                errores.append(f"{tag}: opciones repetidas")
            c = q.get("correcta")
            if not isinstance(c, int) or not 0 <= c < len(ops):
                errores.append(f"{tag}: 'correcta' fuera de rango")
                continue

            fuente = q.get("fuente") or {}
            doc, cita = fuente.get("documento"), fuente.get("cita", "")
            if not doc or not cita:
                errores.append(f"{tag}: falta fuente.documento o fuente.cita")
                continue
            if doc not in textos:
                errores.append(f"{tag}: documento '{doc}' no existe en temario/")
                continue
            cita_n = normalizar(cita)
            if len(cita_n) < MIN_CITA:
                errores.append(f"{tag}: cita demasiado corta (<{MIN_CITA} caracteres)")
                continue
            if cita_n not in textos[doc]:
                errores.append(f"{tag}: la cita NO aparece literal en {doc}")
                continue

            clave = palabras(ops[c])
            if clave:
                solape = len(clave & palabras(cita)) / len(clave)
                if solape < UMBRAL_SOLAPE:
                    avisos.append(f"{tag}: respuesta correcta con solape {solape:.0%} "
                                  f"con la cita — verificar a mano")

    if not quiet or errores:
        for a in avisos:
            print(f"[AVISO]   {a}")
        for e in errores:
            print(f"[BLOQUEO] {e}")
        estado = "RECHAZADO" if errores else "OK"
        print(f"Integridad temario: {estado} · {len(manifest)} quiz · {total} preguntas · "
              f"{len(errores)} bloqueos · {len(avisos)} avisos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
