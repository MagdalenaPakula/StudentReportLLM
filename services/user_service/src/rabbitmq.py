import base64
import logging
import os
import sys

import pika
from opentelemetry import trace
from opentelemetry.trace import Span, SpanKind
from pika.spec import BasicProperties

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


def _get_publish_queue() -> str:
    queue_name = os.getenv('RABBITMQ_PUBLISH_QUEUE')
    if queue_name is None:
        logging.fatal('Environment variable PUBLISH_QUEUE is not set')
        sys.exit(1)
    return queue_name


_publish_queue = _get_publish_queue()


def send_file(file_id: str, file_name: str, file_contents: bytes) -> None:
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
            with tracer.start_as_current_span('Base64 encode'):
                document_body_b64 = base64.b64encode(file_contents)
            logger.debug(f"Converted message body {file_contents} to base 64: {document_body_b64}")
        except Exception as e:
            logger.error("Error while encoding file to base64: " + str(e))
            span.record_exception(e, escaped=True)
            raise
        try:
            message_body_size = len(document_body_b64)
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
                    'x-file-name': file_name,
                    'x-file-id': file_id,
                },
            )
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                properties=properties,
                body=document_body_b64,
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
