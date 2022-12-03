# pip install adtk
# adtk要求輸入數據的索引必須是DatetimeIndex
import numpy as np
import pandas as pd
from influxdb import InfluxDBClient

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from adtk.data import validate_series
from adtk.transformer import DoubleRollingAggregate

torch.manual_seed(1)


class DBApi():
    """Instantiate the connection to the InfluxDB client."""
    def __init__(self,token,org,bucket):
        self._org = org 
        self._bucket = bucket
        self._token = token
        self._client = InfluxDBClient(url="http://localhost:8086", token=self._token, org=self._org, debug=False)

    def query_data(self, query):
        query_api = self._client.query_api()
        result = query_api.query(org=self._org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_value(), record.get_field()))
        print(results)
        return results

class DataPreprocessing():
    def __init__(self):
        pass

    def data_process_for_IMS_bearing(data, separation=0.7, point=2048):
        data = data.reshape(-1,point)
        ratio = int(data.shape[0]*separation)
        training_set = data[:ratio,:]
        testing_set = data[ratio:,:]
        return training_set,testing_set, data


class ML_Engine():
    def __init__(self):
        pass

    #reshape the dataframe according to the LSTM input shape
    def reshape_lstm(self, X, timesteps=1, dim=4):
    # reshape inputs for LSTM [samples, timesteps, features]
    # X: data
    # timesteps: int with number of timesteps
    # dim: int with number ot timesteps
        X_reshape = X.reshape(X.shape[0], timesteps, X.shape[1])
        print('Data shape: ', X_reshape.shape)
        return X_reshape

    def creat_model(self):
        lstm = nn.LSTM(3, 3)  # Input dim is 3, output dim is 3
        inputs = [torch.randn(1, 3) for _ in range(5)]  # make a sequence of length 5

        # initialize the hidden state.
        hidden = (torch.randn(1, 1, 3),
                torch.randn(1, 1, 3))
        for i in inputs:
            # Step through the sequence one element at a time.
            # after each step, hidden contains the hidden state.
            out, hidden = lstm(i.view(1, 1, -1), hidden)
        
        inputs = torch.cat(inputs).view(len(inputs), 1, -1)
        hidden = (torch.randn(1, 1, 3), torch.randn(1, 1, 3))  # clean out hidden state
        out, hidden = lstm(inputs, hidden)
        print(out)
        print(hidden)