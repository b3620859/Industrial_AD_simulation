# import pkg
import os
from datetime import date

from flask import Flask
from flask import request
from flask_httpauth import HTTPBasicAuth

import paho.mqtt.client as mqtt
import json

# Global Variables
MQTT_SERVER = "192.168.1.102"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "msg_v1.0/alert"

# MQTT連線設定
# 初始化地端程式
client = mqtt.Client()
app = Flask(__name__)
auth = HTTPBasicAuth()
# http basic auth credentials
users = {
    "user": "password"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('./alert', methods=['POST'])
@auth.login_required
def alert():
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
    data = json.loads(request.data.decode('utf-8'))
    if data['state'] == 'alerting':
        client.publish(topic=MQTT_TOPIC, payload="1", retain=True)
    elif data['state'] == 'ok':
        client.publish(topic=MQTT_TOPIC, payload="0", retain=True)
    client.disconnect()
    return "ok"

if __name__ == "__main__":
    app.run(host='localhost')