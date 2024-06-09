from flask import Flask, render_template, request

from src.converters.convert import convert_to_txt

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
                return f"Converted text: {text}"
            except Exception as e:
                return f"Error: {str(e)}"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


