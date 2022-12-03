import matplotlib.pyplot as plt
import json

from influxdb import InfluxDBClient

client = InfluxDBClient('54.227.227.143', 8086, 'root', '', 'Sensor')

# 將從資料庫select到的資料取內容(get_points())再將型態轉成list
result = list(client.query('select * from Temperature').get_points())
print(result)

time =[]
tem = []
for item in result:
    # 時間部分只取小分秒的地方
    time.append(item["time"][11:19])
    tem.append(item["Tem"])

# 畫圖
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.plot(time, tem ,'b-o')
plt.show()