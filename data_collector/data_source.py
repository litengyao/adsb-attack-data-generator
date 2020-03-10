"""
@function: executor to get normal data from opensky-network
@author: Li Tengyao
@date: 2018/09/10
"""

from data_collector.opensky_data import OpenskyData

generator = OpenskyData(path="../data/")

# get real time data
# generator.receiveRealTimeData(path="../data/", filename="data.csv", period=240)

# get batch time data
generator.batchReceiveData(date="2019-12-23", start_hour=0, stop_hour=24)
