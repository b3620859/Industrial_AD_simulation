# import pkg
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt

import argparse
import random
import json

# Global Variables
INFLUXDB_ADDRESS = '192.168.1.102'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = 'admin123'
INFLUXDB_DATABASE = 'iot_db'

MQTT_SERVER = "192.168.1.102"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "msg_v1.0/info"

MQTT_REGEX = 'msg_v1.0/([^/]+)'

# generate client ID with pub prefix randomly
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
connected = False  # Stores the connection status

# InfluxDB config
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None,
                                    # ssl=True, verify_ssl=True
                                    )

# class SensorData(NamedTuple):
#     topic_msg: str
#     version: str
#     measurement: str
#     value: float

# InfluxDB連線設定
def _init_influxdb():
    """Instantiate a connection to the InfluxDB."""
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
        print("create new database")
    # 切換至對應資料庫
    influxdb_client.switch_database(INFLUXDB_DATABASE)

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print("Connected with result code "+str(rc))
    if rc == 0:
        print("[INFO] Connected to MQTT Broker!")
        connected = True  # Signal connection for debugg
        # 如果我們失去連線或重新連線時
        # 地端程式將會重新訂閱
        # Subscribe to a topic
        # 將訂閱主題寫在on_connet中
        client.subscribe(MQTT_TOPIC)
    else:
        print("[INFO] Error, connection failed and result code "+str(rc))

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server."""
    # 轉換編碼utf-8用以顯示中文
    print(msg.topic+" "+ msg.payload.decode('utf-8'))
    savedata(msg.topic , msg.payload.decode('utf-8'))

def savedata(topic, data):
    # current_time = datetime.datetime.utcnow().isoformat()
    data = json.loads(data)
    json_body = [
        {
            "measurement": "test",
            "tags": {
                "version": "msg_v1.0",
                "topic": topic
            },
            "fields": data
        }
    ]
    # print("Write points: {0}".format(json_body))
    # 寫入數據至Database
    influxdb_client.write_points(json_body)
    result = influxdb_client.query('select value from test;')
    print("Result: {0}".format(result))


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    _init_influxdb()

    # 連線設定
    # 初始化地端程式
    client = mqtt.Client()
    # 設定連線的動作
    client.on_connect = on_connect
    # 設定接收訊息的動作
    client.on_message = on_message
    # 設定登入帳號密碼
    # client.username_pw_set("try","xxxx")

    print('[INFO] MQTT to InfluxDB bridge')
    # 設定連線資訊(IP, Port, 連線時間)
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
    # 開始連線，執行設定的動作和處理重新連線問題
    # 也可以手動使用其他loop函式來進行連接
    client.loop_forever()
