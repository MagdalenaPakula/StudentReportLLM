import logging

from flask import Flask, render_template, request
from flask_http_middleware import MiddlewareManager
from opentelemetry import trace

from conversion.convert import convert_to_txt
from conversion.logging import configure_logging
from conversion.messaging.rabbitmq import publish_message
from middleware import RequestTimingMiddleware

tracer = trace.get_tracer(__name__)

configure_logging()
app = Flask(__name__)
app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(RequestTimingMiddleware)


@app.route('/', methods=['GET', 'POST'])
def index():
    logger = logging.getLogger(__name__ + '.index')
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = file.filename
            file.save(file_path)
            try:
                text = convert_to_txt(file_path)
                publish_message(exchange_name='logs', routing_key='', message=text)
                return f"Converted text: {text}"
            except Exception as e:
                logger.error(e)
                return f"Error: {str(e)}"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
