import base64
import logging

import pika.channel
import pika.spec
from opentelemetry import trace
from opentelemetry.trace.span import Span

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


def handle_message(channel: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                   properties: pika.spec.BasicProperties, body: bytes):
    message_id = properties.message_id
    correlation_id = properties.correlation_id
    with tracer.start_as_current_span(f"Handle {message_id}") as span:
        span: Span
        try:
            logger.info(f"Handling message {message_id} with correlation_id {correlation_id}")
            document_body = base64.b64encode(body)
            logger.debug(f"Document body: {document_body}")

            # todo: Convert to text format
            # todo: Save to mongo
            # todo: publish message to rabbitmq

        except Exception as e:
            span.record_exception(e, escaped=False)
            return

        logger.info(f"Successfully handled message {message_id}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
