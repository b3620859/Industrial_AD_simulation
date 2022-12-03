# import pkg
import paho.mqtt.client as mqtt
import json
import datetime
import time
import random

import data_utils

# Global Variables
MQTT_SERVER = "192.168.1.102"
MQTT_PORT = 1883  # 8883
MQTT_ALIVE = 60
MQTT_TOPIC = "msg_v1.0/info"

# generate client ID with pub prefix randomly
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
# MQTT_USER = 'iotuser'
# MQTT_PASSWORD = 'iotpassword'

def connect_mqtt():
    # 當地端程式連線伺服器得到回應時，要做的動作
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[INFO] Connected to MQTT Broker!")
        else:
            print("[INFO] Error, connection failed, return code"+str(rc))
    # 連線設定
    # 初始化地端程式
    client = mqtt.Client(MQTT_CLIENT_ID)
    # 設定登入帳號密碼
    # client.username_pw_set("try","xxxx")
    # 設定連線資訊(IP, Port, 連線時間)
    client.on_connect = on_connect
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
    return client

def mqtt_publish(client):
    data1 = data_utils.get_random_data()
    data2 = random.randint(10,30)
    payload = {
        'Sensor1' : data1 ,
        'Sensor2' : data2
    }
    print(json.dumps(payload))
    try:
        #要發布的主題和內容
        client.publish(MQTT_TOPIC, json.dumps(payload))
        # client.loop(2,10) #???
    except Exception as e:
        print("[ERROR] Could not publish data, error: {}".format(e))


if __name__ == "__main__":
    print('[INFO] Sensor Data publish by MQTT...')
    mqtt_client = connect_mqtt()
    while True:
        mqtt_publish(mqtt_client)
        time.sleep(2)
