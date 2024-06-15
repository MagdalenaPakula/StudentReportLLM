from src.GUI import app
from src.logging.logstash_logger import LogStashLogger

from src.messaging.rabbitmq import consume_messages, publish_message


def consume_task_message(ch, method, properties, body):
    logger = LogStashLogger.get_logger()
    logger.info(f'Consumed Message: {body} | Channel {ch} | Method: {method} | Properties: {properties}')


if __name__ == '__main__':
    # Publish a message to the RabbitMQ exchange
    publish_message(exchange_name='my_exchange', routing_key='my_queue', message='Hello, RabbitMQ!')

    # Consume messages from the RabbitMQ queue
    consume_messages(queue_name='my_queue', callback=consume_task_message)

    app.run(host='localhost', port=5000, debug=True)
