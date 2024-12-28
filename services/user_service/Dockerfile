FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN ["opentelemetry-bootstrap", "-a", "install"]

# copy the current service source code
COPY . .

EXPOSE 5000

# Run the Flask application with opentelemetry instrumentation
CMD ["opentelemetry-instrument", "flask", "run", "--host=0.0.0.0"]