import logging

from conversion.handler import handle_message
from conversion.messaging import consume_conversion_requests


def _main():
    configure_logging()
    try:
        logging.info("Starting conversion service")
        consume_conversion_requests(handle_message)
        logging.fatal("Service stopped")
    except Exception as e:
        logging.fatal(f"Exception: {e}")
        raise


def configure_logging():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s <%(name)s> [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    # set log levels
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger('pika').setLevel(logging.WARNING)


if __name__ == '__main__':
    print("Hello")
    _main()
