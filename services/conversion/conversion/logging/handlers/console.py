import logging
from typing import Optional


def add_console_handler(logger: logging.Logger, loglevel: Optional[int] = None) -> None:
    handler = logging.StreamHandler()
    if loglevel is not None:
        handler.setLevel(loglevel)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
