"""
Celery configuration for ArcaTTS.
Shared by all modules (TTS, Grammar, Translator).
"""
from celery import Celery
from shared.config import redis_config

app = Celery('arcatts')

app.config_from_object({
    'broker_url': redis_config.url,
    'result_backend': redis_config.url,
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
    'task_track_started': True,
    'task_time_limit': 3600,
    'worker_prefetch_multiplier': 1,
})

app.autodiscover_tasks([
    'modules.tts.tasks',
    'modules.grammar.tasks',
    'modules.translator.tasks',
])
