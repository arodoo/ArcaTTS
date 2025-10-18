"""
Celery translation tasks.
Async translation for large volumes.
"""
from typing import Optional

from infrastructure.celery.celeryconfig import app
from .base import TranslationTask


@app.task(
    base=TranslationTask,
    bind=True,
    name='translator.translate_text'
)
def translate_text_task(
    self,
    text: str,
    target_language: str,
    source_language: Optional[str] = None
) -> dict:
    """Async text translation."""
    translation = self.service.translate_text(
        text,
        target_language=target_language,
        source_language=source_language
    )

    self.cache.save(translation)

    return {
        'translation_id': str(translation.translation_id),
        'final_translation': translation.final_translation,
        'chunk_count': len(translation.chunks),
        'glossary_terms': len(translation.glossary),
    }


@app.task(
    base=TranslationTask,
    bind=True,
    name='translator.translate_file'
)
def translate_file_task(
    self,
    input_path: str,
    output_path: str,
    target_language: str,
    source_language: Optional[str] = None
) -> dict:
    """Async file translation."""
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    result = translate_text_task.apply(
        args=(text, target_language, source_language)
    ).get()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['final_translation'])

    return result
