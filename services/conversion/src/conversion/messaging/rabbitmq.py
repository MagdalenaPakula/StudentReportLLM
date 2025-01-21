import logging
import os
import sys
from typing import Callable
import base64

import pika
import pika.channel
import pika.spec
from pika.spec import BasicProperties
from opentelemetry import trace
from opentelemetry.trace import Span, SpanKind


logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


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


def _get_publish_queue() -> str:
    env_var_name = 'RABBITMQ_PUBLISH_QUEUE'
    queue_name = os.getenv(env_var_name)
    if queue_name is None:
        logging.fatal(f'Environment variable {env_var_name} is not set')
        sys.exit(1)
    return queue_name


_recv_queue = _get_recv_queue()

_publish_queue = _get_publish_queue()

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



def send_file(file_id: str) -> None:
    exchange_name = ''
    routing_key = _publish_queue

    with tracer.start_as_current_span(f'publish {exchange_name}', kind=SpanKind.PRODUCER, attributes={
        'messaging.operation.type': 'send',
        'messaging.system': 'rabbitmq',
        'messaging.destination.name': exchange_name,
        'messaging.destination.routing_key': routing_key,
    }) as span:
        span: Span
        try:
            logger.debug(f"Message containing {file_id} sent to retrive data.")
        except Exception as e:
            logger.error("Error")
            span.record_exception(e, escaped=True)
            raise
        try:
            message_body_size = len('')
            span.set_attribute('messaging.message.body.size', message_body_size)

            connection = pika.BlockingConnection(_connection_parameters)
            span.add_event('Connection created')

            channel = connection.channel()
            channel.queue_declare(queue=_publish_queue)
            span.add_event('Queue ready')

            properties = BasicProperties(
                content_encoding='base64',
                content_type='application/octet-stream',
                headers={
                    'x-file-id': file_id,
                },
            )
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                properties=properties,
                body =''
            )

            span.add_event("Message published")
            logger.info(f"File published to rabbitmq exchange {exchange_name} with key {routing_key}")
        except Exception as e:
            logger.error("Error while sending file to rabbitmq: " + str(e))
            span.record_exception(e, escaped=True)
            raise
        finally:
            if channel is not None and channel.is_open:
                channel.close()
            if connection is not None and connection.is_open:
                connection.close()
