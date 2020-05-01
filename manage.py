import RPi.GPIO as GPIO
import dht11
import paho.mqtt.client as mqtt
import forecastio
import json
import urllib.request as ur
import os
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

def getRoomData():
    instance = dht11.DHT11(pin = 17)
    result = instance.read()
    if result.is_valid():
        temperature = float(result.temperature) * 9/5.0 + 32
        humidity = float(result.humidity)
        client = mqtt.Client('dht')
        client.connect(str(os.environ['MQTT_SERVER']))
        client.publish("DHT/temperature", str(temperature))
        client.publish("DHT/humidity", str(humidity))
    else:
        sys.stderr.write(str(result.error_code) + '\n')

def getDSData():
    api_key = str(os.environ['DS_API_KEY'])
    lat = str(os.environ['DS_LAT'])
    lng = str(os.environ['DS_LNG'])

    forecast = forecastio.load_forecast(api_key, lat, lng)
    currently = forecast.currently()
    temperature = currently.temperature
    humidity = float(currently.humidity) * 100

    client = mqtt.Client('darksky')
    client.connect(str(os.environ['MQTT_SERVER']))
    client.publish("Darksky/temperature", str(temperature))
    client.publish("Darksky/humidity", str(humidity))

def publishMQTT(topic, value):
    client = mqtt.Client('dht')
    client.connect(str(os.environ['MQTT_SERVER']))
    client.publish(topic, value)

def getPresenceData():
    url = "https://mohawk.doubleangels.com/fingLog/output.json"
    response = ur.urlopen(url)
    json_data = json.loads(response.read())

    up_devices = []
    down_devices = []
    for host in json_data['Hosts']:
        if host['State'] == 'up':
            up_devices.append(host['Name'])

    matt_devices = ['Aphrodite', 'Chaos']
    chris_devices = ['Chris Phone', 'Chris Laptop']
    geno_devices = ['Geno Phone', 'Geno PC']
    tyler_devices = ['Tyler Phone', 'Tyler PS4']
    taylor_devices = ['Taylor Phone', 'Taylor PS4']

    matt_up = []
    chris_up = []
    geno_up = []
    tyler_up = []
    taylor_up = []

    for device in up_devices:
        for matt_device in matt_devices:
            if matt_device in device:
                matt_up.append(device)

    for device in up_devices:
        for chris_device in chris_devices:
            if chris_device in device:
                chris_up.append(device)

    for device in up_devices:
        for geno_device in geno_devices:
            if geno_device in device:
                geno_up.append(device)

    for device in up_devices:
        for tyler_device in tyler_devices:
            if tyler_device in device:
                tyler_up.append(device)

    for device in up_devices:
        for taylor_device in taylor_devices:
            if taylor_device in device:
                taylor_up.append(device)

    if len(matt_up) >= 1:
        publishMQTT('Presence/matt', len(matt_up))
    else:
        publishMQTT('Presence/matt', 0)

    if len(chris_up) >= 1:
        publishMQTT('Presence/chris', len(chris_up))
    else:
        publishMQTT('Presence/chris', 0)

    if len(geno_up) >= 1:
        publishMQTT('Presence/geno', len(geno_up))
    else:
        publishMQTT('Presence/geno', 0)

    if len(tyler_up) >= 1:
        publishMQTT('Presence/tyler', len(tyler_up))
    else:
        publishMQTT('Presence/tyler', 0)

    if len(taylor_up) >= 1:
        publishMQTT('Presence/taylor', len(taylor_up))
    else:
        publishMQTT('Presence/taylor', 0)

counter = 0
while True:
    getRoomData()
    counter += 1
    if counter == 5:
        getDSData()
        counter = 0
    getPresenceData()
    time.sleep(60)