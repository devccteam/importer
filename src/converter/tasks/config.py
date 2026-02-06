from datetime import timedelta
from typing import Final

from celery import Celery

from converter.settings import settings

redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT

broker = f'redis://{redis_host}:{redis_port}/0'

TASK_PACKAGES: Final[list[str]] = [
    'converter.tasks.processa',
    'converter.tasks.clear_db',
]

celery = Celery('tasks', broker=broker, backend=broker)


celery.autodiscover_tasks(TASK_PACKAGES)

celery.conf.beat_schedule = {
    'clean_db': {
        'task': 'clear_db',
        'schedule': timedelta(days=3),
    },
}

celery.conf.timezone = 'UTC'
