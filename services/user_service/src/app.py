import logging
import uuid

from flask import Flask, render_template, request, jsonify
from flask_http_middleware import MiddlewareManager
from opentelemetry import trace

from middleware import RequestTimingMiddleware
from rabbitmq import send_file

# OpenTelemetry setup
tracer = trace.get_tracer(__name__)

# Flask app setup
app = Flask(__name__)
app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(RequestTimingMiddleware)

upload_status = {}
embedding_status = {}

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

        # Generate a unique ID for the file
        file_id = str(uuid.uuid4())

        # Send file to RabbitMQ for processing
        send_file(file_id, file_name, file_contents)
        app.logger.info(f"File {file_name} sent to RabbitMQ with ID {file_id}")

        # HTTP 202 - Accepted, because file is sent for further processing, but not yet processed
        return jsonify(message='Request accepted', file_id=file_id), 202
    except Exception as e:
        app.logger.error(str(e))
        return f"Internal error: {str(e)}", 500


@app.route('/status/<file_id>', methods=['GET'])
def get_upload_status(file_id):
    try:
        if file_id not in upload_status:
            return jsonify({"message": "File not found"}), 404

        return jsonify({"file_id": file_id, "status": upload_status[file_id]["status"]}), 200
    except Exception as e:
        app.logger.error(f"Error fetching status for {file_id}: {str(e)}")
        return f"Internal error: {str(e)}", 500


@app.route('/embedding-status/<file_id>', methods=['GET'])
def get_embedding_status(file_id):
    try:
        if file_id not in embedding_status:
            return jsonify({"message": "Embedding not found"}), 404

        return jsonify({"file_id": file_id, "status": embedding_status[file_id]["status"]}), 200
    except Exception as e:
        app.logger.error(f"Error fetching embedding status for {file_id}: {str(e)}")
        return f"Internal error: {str(e)}", 500

def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    app.logger.setLevel(logging.NOTSET)

    # setup console logging
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s <%(name)s> [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

def create_app() -> Flask:
    configure_logging()
    app.logger.info("Starting user service")
    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=False)
