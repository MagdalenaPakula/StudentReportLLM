import logging

from flask import Flask, render_template, request
from flask_http_middleware import MiddlewareManager
from opentelemetry import trace

from conversion.logging import configure_logging
from middleware import RequestTimingMiddleware

tracer = trace.get_tracer(__name__)

configure_logging()
app = Flask(__name__)
app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(RequestTimingMiddleware)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Request does not contain file', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    file.save(f"/tmp/uploads/{file.filename}")

    # todo: Assign unique ID for this work
    # todo: Publish file to rabbitmq

    # HTTP 202 - Accepted, because file is sent for further processing, but not yet processed
    return 'Request accepted', 202

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
