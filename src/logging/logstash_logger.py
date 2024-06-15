import json
import logging
import os
from logstash_async.handler import AsynchronousLogstashHandler


class LogStashLogger:
    _instance = None

    @staticmethod
    def get_logger():
        if LogStashLogger._instance is None:
            LogStashLogger()
        return LogStashLogger._instance

    def __init__(self):
        if LogStashLogger._instance is not None:
            raise Exception("LoggerSingleton must be a singleton")
        else:
            LogStashLogger._instance = self._configure_logger()

    def _configure_logger(self):
        host = os.getenv('LOGSTASH_HOST', 'localhost')
        port = int(os.getenv('LOGSTASH_PORT', 5044))

        logger = logging.getLogger('logstash-python-logger')
        logger.setLevel(logging.INFO)

        logstash_handler = AsynchronousLogstashHandler(host, port, database_path=None)
        json_formatter = JsonLogstashFormatter(datefmt='%Y-%m-%dT%H:%M:%S%z')
        logstash_handler.setFormatter(json_formatter)
        logger.addHandler(logstash_handler)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        return logger


class JsonLogstashFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(log_record)