# ArcaTTS - Comandos Rápidos

## Comandos

```bash
# 1. Parsear libro (generar manifest)
python -m modules.tts.cli parse boocks/libro.txt --verbose

# 2. Probar una obra
python -m modules.tts.cli process-work outputs/manifests/libro_manifest.json 1 --output outputs/autor

# 3. Procesar todo el libro
python -m modules.tts.cli process-all outputs/manifests/libro_manifest.json --output outputs/autor --workers 1 --start-from 1

# 4. Reanudar desde obra N
python -m modules.tts.cli process-all outputs/manifests/libro_manifest.json --output outputs/autor --workers 1 --start-from 25

# 5. Test rápido
python -m modules.tts.cli test --text "Prueba. Con pausas."
```

## Formato del archivo .txt

```
ÍNDICE
$TÍTULO OBRA (1920)
$OTRA OBRA (1925)
FIN DEL ÍNDICE
```

## Útiles

```bash
# Ver progreso
ls outputs/autor/ | wc -l

# Limpiar
rm -rf outputs/autor/*

# Regenerar obra específica
rm -rf outputs/autor/50_TITULO
python -m modules.tts.cli process-work outputs/manifests/libro_manifest.json 50 --output outputs/autor



```

## Configuración

- **Pausas:** Punto 0.7s, Coma 0.3s, Diálogo -¿...?- 0.4s
- **MP3:** 128kbps (~75% ahorro vs WAV)
- **Tiempo:** ~2-5 min por obra pequeña, ~4.5h para 54 obras

- **Correr el test pipeline:**
python -m modules.tts.tests.test_chapter

Más detalles: `.github/instructions/project-reference.instructions.md`
