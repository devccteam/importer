import atexit
import json
import logging
from logging.config import dictConfig
from pathlib import Path

ROOT_DIR = Path('.')
LOGS_DIR = ROOT_DIR / 'logs'
LOG_CONFIG_PATH = ROOT_DIR / 'src/converter/logging.json'


def setup(logger_name: str) -> logging.Logger:
    if not LOGS_DIR.is_dir():
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    with LOG_CONFIG_PATH.open(encoding='utf8') as file:
        logging_config = json.load(file)

    dictConfig(logging_config)

    queue_handler = logging.getHandlerByName('queue')
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

    return logging.getLogger(logger_name)
