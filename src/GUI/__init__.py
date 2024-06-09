from flask import Flask, render_template, request

from src.convertion.convert import convert_to_txt
from src.messaging.rabbitmq import publish_message

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
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
                return f"Error: {str(e)}"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
