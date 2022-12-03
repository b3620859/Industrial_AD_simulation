import numpy as np
import datetime
import time
import random

from faker import Faker

# Global Variables
DATASET_PATH  = '/home/cslab/Documents/'
data_dir = '2nd_data.npz'
window_size = 2048

def load_bearingData(data_class=0, point=2048):
    # Load Data
    bearing_data = np.load(DATASET_PATH+data_dir)['data'][:,:,data_class]
    # Reshape
    bearing_data = bearing_data.reshape(-1,point,1)
    return bearing_data


# bearing2_data_rms1 = np.array(np.sqrt(np.mean(np.power(bearing2_data1, 2), axis=1)))
# bearing2_data_rms2 = np.array(np.sqrt(np.mean(np.power(bearing2_data2, 2), axis=1)))
# bearing2_data_rms3 = np.array(np.sqrt(np.mean(np.power(bearing2_data3, 2), axis=1)))
# bearing2_data_rms4 = np.array(np.sqrt(np.mean(np.power(bearing2_data4, 2), axis=1)))

# data_merged = np.concatenate((bearing2_data_rms1, bearing2_data_rms2, bearing2_data_rms3, bearing2_data_rms4), axis=1)

# bearing2_data_rms = pd.DataFrame(data_merged)
# bearing2_data_rms.columns = ['Bearing 1', 'Bearing 2', 'Bearing 3', 'Bearing 4']

# def data_process_for_IMS_bearing(data, separation=0.7):
#     ratio = int(data.shape[0]*separation)
#     training_set = data[:ratio]
#     testing_set = data[ratio:]
#     return training_set,testing_set, data

# train_ratio = 0.1
# bearing2_train, bearing2_test = data_process_for_IMS_bearing(bearing2_data_rms, train_ratio)
# print(bearing2_data_rms.shape)
# print(bearing2_train.shape)
# print(bearing2_test.shape)


# # ----------------
# target_size = 100
# freq = 5
# train_ratio = 1
# def data_process_for_IMS_bearing(data, separation=0.7, point=2048):
#     data = data.reshape(-1,point)
#     ratio = int(data.shape[0]*separation)
#     training_set = data[:ratio,:]
#     testing_set = data[ratio:,:]
#     return training_set,testing_set, data


# training, _, full_data = data_process_for_IMS_bearing(data,train_ratio,window_size)
# print(training.shape)
# print(full_data.shape)

# --------------------

# 設置日期時間的格式
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
# Init Faker, our fake data provider
fake = Faker()

def sine_wave():
    time = np.arange(0, 200, 0.1)
    sin = np.sin(time) + np.random.normal(scale=0.5, size=len(time))

    sin_1 = np.sin(time) + np.sin(3*time)/3 + np.sin(5*time)/5
    return sin

def get_date():
    date = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    return date

def get_sine_wave():
    output_data = sine_wave()
    for output in output_data:
        print(output)
        print(get_date())
        time.sleep(0.5)

def get_random_data():
    data = random.randint(0, 100)
    return data

def get_fake_data():
    temperature = fake.random_int(min=0, max=30)
    return temperature
