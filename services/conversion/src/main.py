import logging

from conversion.handler import handle_message
from conversion.messaging import consume_conversion_requests

 
def try_start_with_retries(num_retries: int) -> None:
    import pika.exceptions
    import time

    timeout_seconds: float = 1.0
    failed_attempts = 0
    while True:
        try:
            consume_conversion_requests(handle_message)
            return
        except pika.exceptions.AMQPConnectionError:
            if failed_attempts >= num_retries:
                logging.fatal(f"Failed to connect to rabbitmq in {failed_attempts} attempts, aborting")
                raise
            logging.warning(f"Failed to connect to rabbitmq, retrying in {timeout_seconds} seconds.")
            failed_attempts += 1
            time.sleep(timeout_seconds)


def _main():
    configure_logging()
    try:
        logging.info("Starting conversion service")
        try_start_with_retries(num_retries=3)
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
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('pika').setLevel(logging.WARNING)


if __name__ == '__main__':
    print("Hello")
    _main()
