FROM arm32v6/python:3.8-alpine3.11

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

WORKDIR /app
ADD . /app

CMD ["python", "manage.py"]
