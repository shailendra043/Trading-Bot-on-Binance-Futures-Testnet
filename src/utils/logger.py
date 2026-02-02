import logging
import json
from logging import Logger
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'module': record.module,
            'message': record.getMessage(),
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def get_logger(name: str = 'bot', log_file: str = 'bot.log') -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger
