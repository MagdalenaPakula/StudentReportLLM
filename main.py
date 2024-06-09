from src.GUI import app

from src.messaging.rabbitmq import consume_messages, publish_message


def consume_task_messages(ch, method, properties, body):
    print(f" [x] Received message: {body}")


if __name__ == '__main__':
    # Publish a message to the RabbitMQ exchange
    publish_message(exchange_name='my_exchange', routing_key='my_queue', message='Hello, RabbitMQ!')

    # Consume messages from the RabbitMQ queue
    consume_messages(queue_name='my_queue', callback=consume_task_messages)

    app.run(host='localhost', port=5000, debug=True)
