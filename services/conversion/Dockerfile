FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy shared code
COPY lib lib

# copy the current service source code
COPY services/conversion services/conversion

# Set the FLASK_APP environment variable
ENV FLASK_APP=services.conversion

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
