import logging
import os
import sys
from typing import Callable

import pika
import pika.channel
import pika.spec


def _get_connection_parameters() -> pika.ConnectionParameters:
    host = os.getenv('RABBITMQ_HOST')
    if host is None:
        logging.fatal('Environment variable RABBITMQ_HOST is not set')
        sys.exit(1)

    port = os.getenv('RABBITMQ_PORT')
    if port is None:
        logging.fatal('Environment variable RABBITMQ_PORT is not set')
        sys.exit(1)

    return pika.ConnectionParameters(host=host, port=port)


# cache the connection parameters value
_connection_parameters = _get_connection_parameters()


def _get_recv_queue() -> str:
    env_var_name = 'RABBITMQ_RECV_QUEUE'
    queue_name = os.getenv(env_var_name)
    if queue_name is None:
        logging.fatal(f'Environment variable {env_var_name} is not set')
        sys.exit(1)
    return queue_name


_recv_queue = _get_recv_queue()

Callback = Callable[
    [
        pika.channel.Channel,
        pika.spec.Basic.Deliver,
        pika.spec.BasicProperties,
        bytes
    ],
    None
]


def consume_conversion_requests(callback: Callback):
    logger = logging.getLogger(__name__)

    logger.debug(f"Trying to connect to {_connection_parameters}")
    connection = pika.BlockingConnection(_connection_parameters)
    logger.debug(f"Connection established")
    channel = connection.channel()
    channel.queue_declare(queue=_recv_queue)
    channel.basic_consume(queue=_recv_queue, on_message_callback=callback, auto_ack=False)
    logger.info(f'Listening for messages on queue {_recv_queue}')
    channel.start_consuming()
