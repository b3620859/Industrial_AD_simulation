# Industrial anomaly detection simulation
MQTT Streaming Data Source for Grafana and Jetson Nano.

## How to Set up and Use.
+ Docker Setup(for Edge device)
```shell
$ sudo docker pull nvcr.io/nvidia/l4t-ml:r32.7.1-py3
$ sudo docker run --name=dev_nano --runtime nvidia --network host nvcr.io/nvidia/l4t-ml:r32.7.1-py3
```
+ To run Grafana in a Docker container, with this plugin included:
```shell
$ docker run -d -p 3000:3000 --name=grafana grafana/grafana-oss:8.2.0
```

+ Install mosquitto for Edge device.
```shell
$ sudo apt-get install -y mosquitto mosquitto-clients
```
+ Check mosquitto status
```shell
$ service mosquitto status
```
+ Install mosquitto for Host PC(Ubuntu).
```shell
$ sudo apt-get update
$ sudo apt-get install mosquitto
```
If you need some of the local testing tools giving you the ability to post to and watch incoming messages on topics then go ahead and install the clients too. They’re very handy.
```shell
$ sudo apt-get install mosquitto-clients
```
+ Setting up Mosquitto(for Edge device)
```shell
// Get the IP of the Edge device.
$ hostname -I
// Edit profile.
$ sudo vi /etc/mosquitto/mosquitto.conf

allow_anonymous true
listener 1883 Rpi-IP
```
+ restart mosquitto(for Edge device)
```shell
$ sudo service mosquitto stop
$ sudo service mosquitto start
```
## Setting InfluxDB Database
Python installing InfluxDB Python Client Library.
```shell
$ python3 -m pip install influxdb
```

## Run Test script with Python
+ Activate Python environment.
```shell
// for Windows(powershell)
$ .\venv\Scripts\Activate.ps1
// for MAC/Linux
$ source ./venv/Scripts/Activate
```
+ Install Python Package.
```shell
$ pip install -r requirements.txt
```
+ Install the kit on the Edge device side and the Host PC(Ubuntu) side.
```shell
$ pip install paho-mqtt==1.6.1
```
Run `subscriber.py` for Edge device.
```shell
$ python3 subscriber.py
```
Run `publisher.py` for Host PC.
```shell
$ python3 publisher.py
```
(stop with Ctrl-C/Cmd-C). You can see the script running in the screencast above.
+ MQTT with TLS/SSL encryption


