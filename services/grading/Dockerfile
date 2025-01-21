FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

RUN ["opentelemetry-bootstrap", "-a", "install"]

COPY src .

CMD ["opentelemetry-instrument", "python", "main.py"]
