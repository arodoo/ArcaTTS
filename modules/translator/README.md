# Translator Module

Módulo de traducción local usando MarianMT/Opus-MT.
Prioriza elegancia y fidelidad sobre velocidad.

## Características

- **Traducción local**: Sin APIs externas, sin costos
- **Alta calidad**: Beam search, context-aware translation
- **Consistencia**: Glossary automático para términos
- **Validación**: Post-processing y quality checks
- **Async**: Integración con Celery para volúmenes grandes
- **Cache**: Traducciones guardadas, reinicio sin pérdida

## Instalación

```bash
pip install transformers torch langdetect click
```

## Uso CLI

### Traducir archivo

```bash
python -m modules.translator.cli translate \
  boocks/input.txt \
  boocks/output.txt \
  --target en \
  --source es \
  --use-gpu
```

### Auto-detección de idioma

```bash
python -m modules.translator.cli translate \
  input.txt output.txt --target fr
```

## Uso Programático

```python
from modules.translator.infrastructure.marian_adapter import (
    MarianTranslatorAdapter
)
from modules.translator.application.translation_service import (
    TranslationService
)

translator = MarianTranslatorAdapter(use_gpu=True)
service = TranslationService(translator)

translation = service.translate_text(
    "Texto en español",
    target_language="en"
)

print(translation.final_translation)
```

## Idiomas Soportados

- Español ↔ Inglés
- Español ↔ Portugués (incluye brasileño)
- Francés ↔ Inglés
- Alemán ↔ Inglés
- Italiano ↔ Inglés

## Ejemplo: Español → Portugués Brasileño

```bash
python -m modules.translator.cli translate \
  "boocks/4 América autor Franz Kafka.txt" \
  "boocks/4_America_PT-BR.txt" \
  --source es \
  --target pt \
  --use-gpu
```

**Nota**: El modelo `opus-mt-es-pt` traduce a portugués
estándar que funciona perfectamente para brasileño.
