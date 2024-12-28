import json
import logging
from os import getenv
from typing import Optional

from logstash_async.handler import AsynchronousLogstashHandler


class _JsonLogstashFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(log_record)


def add_logstash_handler(logger: logging.Logger, log_level: Optional[int] = None) -> None:
    host = getenv('LOGSTASH_HOST', 'localhost')
    port = int(getenv('LOGSTASH_PORT', 5044))

    logger.setLevel(log_level if log_level is not None else logging.INFO)

    logstash_handler = AsynchronousLogstashHandler(host, port, database_path=None)
    json_formatter = _JsonLogstashFormatter(datefmt='%Y-%m-%dT%H:%M:%S%z')
    logstash_handler.setFormatter(json_formatter)
    logger.addHandler(logstash_handler)
