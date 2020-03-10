"""
@function: get the data from outside csv data
@author: Tengyao Li
@date: 2018/09/12
@status: success
"""
import pandas as pd
import numpy as np
import os
from util.parameter import DATA_INPUT_PATH


class reader:
    """
    @function: retain the dataset
    @author: Tengyao Li
    @date: 2018/09/12
    """

    def __init__(self, path=DATA_INPUT_PATH, year=2019, month=12, day=23):
        """
        @function: initialize the path and date
        @author: Tengyao Li
        @date: 2018/09/12
        
        :param path: the csv data source file path
        :param year:  year
        :param month:  month
        :param day:  day
        :return: none
        """
        self.path = path
        self.year = year
        self.month = month
        self.day = day

    def get_hour_data(self, hour=0):
        """
        @function: get the specific hour data
        @author: Tengyao Li
        @date:2018/09/12
        
        :param hour: the specific hour (hour \in [0,23])
        :return: the data frame
        """

        df = pd.DataFrame()
        if hour < 10:
            df = pd.read_csv(
                os.path.join(self.path, 'states_%i-%i-%i-0%i.csv' % (self.year, self.month, self.day, hour)))
        else:
            df = pd.read_csv(
                os.path.join(self.path, 'states_%i-%i-%i-%i.csv' % (self.year, self.month, self.day, hour)))
        return df

    def get_continious_data(self, start_hour=0, end_hour=23):
        """
        @function: get dataset for specific periods
        @author: Tengyao Li
        @date: 2018/09/12
        
        :param start_hour: the beginning hour 
        :param end_hour: the last hour (included)
        :return: the data frame
        """
        df = pd.DataFrame()
        for hour in np.arange(start=start_hour, stop=end_hour+1):
            if hour < 10:
                dfx = pd.read_csv(
                    os.path.join(self.path,
                                 'states_%i-%i-%i-0%i.csv' % (int(self.year), int(self.month), int(self.day), hour)))
            else:
                dfx = pd.read_csv(
                    os.path.join(self.path,
                                 'states_%i-%i-%i-%i.csv' % (int(self.year), int(self.month), int(self.day), hour)))

            df = df.append(dfx, ignore_index=True)

        return df

    def get_specific_flight(self, icao, start_hour=0, end_hour=23):
        """
        @function: get the specific flight with icao24
        @author: Tengyao Li
        @date: 2018/09/12
        
        :param icao: the icao24 identity
        :param start_hour: the beginning hour
        :param end_hour: the last hour
        :return: the data frame for the specific flight
        """

        df = self.get_continious_data(start_hour, end_hour)

        return df.loc[df.icao24 == icao]

    def get_specific_time(self, timestamp, current_hour):
        """
        @function: get the specific time data
        @author: Tengyao Li
        @date: 2018/09/12
        
        :param timestamp: the timestamp
        :param current_hour: used to locate the data file (remove in the future due to deprecation)
        :return: the data frame for the specific time
        """

        df = self.get_hour_data(current_hour)

        return df.loc[df.time == timestamp]

### scripts here!
# scripts = reader()
# df = scripts.get_continious_data(0, 0)
# print(df.head())
# output:
#         time  icao24        lat  ...  geoaltitude  lastposupdate   lastcontact
# 0  1577059200  502cdf  49.472305  ...     11414.76   1.577059e+09  1.577059e+09
# 1  1577059200  4ca848  52.740799  ...     10637.52   1.577059e+09  1.577059e+09
# 2  1577059200  49d3fa  47.854568  ...     10454.64   1.577059e+09  1.577059e+09
# 3  1577059200  4bb847  50.602376  ...     11323.32   1.577059e+09  1.577059e+09
# 4  1577059200  400755        NaN  ...          NaN            NaN  1.577059e+09
#
# [5 rows x 16 columns]
