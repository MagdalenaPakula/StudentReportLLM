import logging

from flask import Flask, render_template, request
from flask_http_middleware import MiddlewareManager
from opentelemetry import trace

from middleware import RequestTimingMiddleware
from rabbitmq import send_file

tracer = trace.get_tracer(__name__)

app = Flask(__name__)
app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(RequestTimingMiddleware)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'Request does not contain file', 400

        file = request.files['file']
        file_name = file.filename
        if file_name == '':
            return 'No file selected', 400

        app.logger.info(f"Received file {file_name}")
        file_contents = file.read()

        # todo: Assign unique ID for this work
        send_file(file_name, file_contents)

        # HTTP 202 - Accepted, because file is sent for further processing, but not yet processed
        return 'Request accepted', 202
    except Exception as e:
        app.logger.error(str(e))
        return f"Internal error: {str(e)}", 500


def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    app.logger.setLevel(logging.NOTSET)

    # setup console logging
    hanlder = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s <%(name)s> [%(levelname)s] %(message)s')
    hanlder.setFormatter(formatter)
    root_logger.addHandler(hanlder)

def create_app() -> Flask:
    configure_logging()
    app.logger.info("Starting user service")
    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=False)
