# Sara Quiz · Examen 100 — reglas del proyecto

## REGLA DURA: integridad del temario (orden del mando, no negociable)
- Cada pregunta y su respuesta correcta se basan **única, exclusiva y únicamente** en el temario
  entregado por Sara (`temario/`). Nada de conocimiento externo, ni "lo que dice la ley vigente",
  ni completar huecos del temario.
- Cada pregunta lleva `fuente.documento` (nombre del .txt en `temario/`) y `fuente.cita`
  (fragmento **literal** del temario que sostiene la respuesta correcta, ≥25 caracteres).
- La respuesta correcta se verifica contra la cita **antes** de escribirla. Los distractores deben ser
  incorrectos según el propio temario, no según fuentes externas.
- Si algo del temario es ambiguo, contradictorio o está marcado como derogado/suprimido: no se pregunta
  como vigente; se consulta al mando.
- Redacción y verificación las ejecuta Captain; no se delegan (precedente sara-quiz-forestal).

## Guardián mecánico (tres cerrojos, mismo validador `tools/validar_integridad.py`)
1. Hook de Claude Code (`.claude/settings.json`, PostToolUse) — valida cada escritura en `data/*.json`.
2. Hook de git (`.githooks/pre-commit`, activado con `core.hooksPath`) — bloquea el commit.
3. Ejecución manual: `python3 tools/validar_integridad.py`.
El validador comprueba que la cita existe literal; la **correspondencia cita↔respuesta** sigue siendo
verificación humana (los avisos de solape bajo obligan a revisarla a mano). No desactivar nunca.

## Flujo al recibir el temario
1. PDF(s) → `temario/` (copiar a nombre ASCII si viene en NFD). `tools/extraer_temario.sh`.
2. Revisar el .txt extraído (cabeceras, pies, saltos) antes de citar.
3. Examen = 1 JSON de 100 preguntas en `data/`, alta en `data/quizzes-manifest.json`.
4. Reglas heredadas: desambiguar cifras múltiples en el enunciado; alternar estilo con preguntas
   negativas ("señale la INCORRECTA") sin uniformarlo; sin duplicados entre exámenes.
5. `temario/` está en `.gitignore`: el material de Sara no se publica. Ningún secreto en el código.

## Formato de pregunta
```json
{"id":"e1-001","pregunta":"…","opciones":["…","…","…"],"correcta":0,
 "explicacion":"Tema X, apartado Y, literal.",
 "fuente":{"documento":"tema-01.txt","cita":"fragmento literal del temario"}}
```
