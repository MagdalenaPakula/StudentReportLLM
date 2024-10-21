import logging

from .handlers.console import add_console_handler
from .handlers.logstash import add_logstash_handler


def configure_logging() -> None:
    """
    This function should be called at the start of the application.
    This is the place to configure handlers and log levels for the service root logger.
    This configuration will be inherited by all created loggers.
    """
    root_logger = logging.getLogger()
    add_console_handler(root_logger)

    logger_settings = {
        'pdfminer': logging.WARNING,
        'pika': logging.WARNING,
        'conversion': logging.DEBUG,
        'app': logging.DEBUG
    }

    for logger_name, log_level in logger_settings.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
