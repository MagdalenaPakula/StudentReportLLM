import base64
import logging
import os
import uuid

import pika.channel
import pika.spec
from opentelemetry import trace
from opentelemetry.trace.span import Span

from conversion.convert import convert_to_txt, save_to_mongo
from conversion.messaging.rabbitmq import send_file

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


def handle_message(channel: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                   properties: pika.spec.BasicProperties, body: bytes):
    message_id = properties.message_id

    with tracer.start_as_current_span(f"Handle {message_id}") as span:
        span: Span
        try:
            logger.info(f"Handling message {message_id}")
            document_body = base64.b64decode(body)
            document_name = properties.headers['x-file-name']
            document_id = properties.headers['x-file-id']

            # add uuid4 at the beginning to prevent collisions
            file_name = f"/tmp/{str(uuid.uuid4())}-{document_name}"
            with open(file_name, "wb") as f:
                logger.debug(f"Writing file contents to {file_name}")
                f.write(document_body)
            document_text = convert_to_txt(file_name)
            logger.debug("Converted document text:\n" + document_text)

            # todo: check the assumption that rabbitmq message id can be used as grading request id
            save_to_mongo(document_id, document_text)

            send_file(document_id)
            logger.debug(f"Removing temporary file {file_name}")
            os.remove(file_name)

        except Exception as e:
            span.record_exception(e, escaped=False)
            return

        logger.info(f"Successfully handled message {message_id}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
