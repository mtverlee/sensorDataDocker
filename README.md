# sensorDataDocker
Collect sensor data for use with MQTT and NodeRed.

## Usage
- ```docker create -e MQTT_SERVER=<hostname> -e DS_API_KEY=<api_key> -e DS_LAT=<latitude> -e DS_LNG=<longitude> --name sensordata --label com.datadoghq.ad.logs="[{"source": "<hostname>", "service": "sensordata"}]" --device /dev/gpiomem -e TZ=America/Denver doubleangels/sensordata:latest```
- ```docker start sensordata```
