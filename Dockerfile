FROM arm32v6/python:3.8-alpine3.11

# Set environment variables.
ARG TZ=America/Denver
ARG MQTT_SERVER=localhost
ARG DS_LAT=39.0732
ARG DS_LNG=-108.4904

# Install dependencies.
RUN apk add git build-base

# Install Adafruit_DHT.
RUN git clone https://github.com/szazo/DHT11_Python.git && \
	cd DHT11_Python && \
	python3 -m pip install .

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

# Set up working directory.
WORKDIR /app
ADD . /app

# Start main python file.
CMD ["python", "manage.py"]
