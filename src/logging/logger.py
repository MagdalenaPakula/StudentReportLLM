import logging
import os
from logstash_async.handler import AsynchronousLogstashHandler


class Logger:
    _instance = None

    @staticmethod
    def get_logger():
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("LoggerSingleton must be a singleton")
        else:
            Logger._instance = _configure_logger()


def _configure_logger():
    host = os.getenv('LOGSTASH_HOST', 'localhost')
    port = int(os.getenv('LOGSTASH_PORT', 5044))

    logger = logging.getLogger('logstash-logger')
    logger.setLevel(logging.INFO)

    logstash_handler = AsynchronousLogstashHandler(host, port, database_path=None)

    logstash_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z'))
    logstash_handler.setLevel(logging.INFO)

    logger.addHandler(logstash_handler)

    return logger


if __name__ == "__main__":
    logger = Logger.get_logger()
    logger.info('Info message')
    logger.warning('Warning message')