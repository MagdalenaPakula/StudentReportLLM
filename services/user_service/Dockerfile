FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN ["opentelemetry-bootstrap", "-a", "install"]

# copy the current service source code
COPY src .

EXPOSE 5000

# Run the Flask application with opentelemetry instrumentation
CMD ["opentelemetry-instrument", "python", "app.py"]