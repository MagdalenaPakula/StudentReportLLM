import os
import pika

from src.logging.logstash_logger import LogStashLogger


logger = LogStashLogger.get_logger()


def publish_message(exchange_name, routing_key, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT'))))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
    logger.info(f'Published Message: {message} | Exchange: {exchange_name} | Routing Key: {routing_key}')
    connection.close()


def consume_messages(queue_name, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT'))))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f' [*] Waiting for messages in queue "{queue_name}". To exit press CTRL+C')
    channel.start_consuming()
