"""
@function: analyze the original ADS-B data on spatial-temporal traits
@author: Tengyao Li
@date: 2018/09/12
@status: success
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

from scipy.spatial.distance import pdist

from util.parameter import DATA_INPUT_PATH

class data_analysis:
    """
    @function: basic analysis on ADS-B data characteristics
    @author: Tengyao Li
    @date: 2018/09/12
    """

    def __init__(self, hour_limitation=1):
        """
        @function: initialize the dataset
        @author: Tengyao Li
        @date: 2018/09/12
        
        @:param hour_limitation: limit the amount of dataset to merge
        """
        # merge dataset for different hours
        self.df = pd.DataFrame()
        for hour in range(hour_limitation):
            if hour < 10:
                dfx = pd.read_csv(DATA_INPUT_PATH + '/states_2019-12-23-0%i.csv' % hour)
            else:
                dfx = pd.read_csv(DATA_INPUT_PATH + '/states_2019-12-23-%i.csv' % hour)

            dfx.time = dfx.time.apply(lambda x: time.strftime("%H:%M:%S", time.localtime(x)))

            self.df = self.df.append(dfx, ignore_index=True)

    def time_relevance_analysis(self, loop=20):
        """
        @function: analyze the time relevance
        @author: Tengyao Li
        @date: 2018/09/12
        
        @:param loop: limit the amount of flights
        :return: none
        """

        variances_lat = np.zeros(loop)
        variances_lon = np.zeros(loop)

        for icao in self.df.icao24.unique():

            df_cruise = self.df.loc[self.df.icao24 == icao]  # get the current flight route

            record_num = df_cruise.lat.shape[0]
            lat_deviation = np.zeros(record_num - 1)
            lon_deviation = np.zeros(record_num - 1)

            for i in range(record_num - 1):
                lat_deviation[i] = df_cruise.lat.iloc[i + 1] - df_cruise.lat.iloc[i]
                lon_deviation[i] = df_cruise.lon.iloc[i + 1] - df_cruise.lon.iloc[i]

            variance_lat = np.var(lat_deviation)
            variance_lon = np.var(lon_deviation)

            if np.isnan(variance_lat) or np.isnan(variance_lon):
                loop += 1
                continue

            variances_lat[loop - 1] = variance_lat
            variances_lon[loop - 1] = variance_lon

            # loop control
            # limit the amount of flights
            loop -= 1
            if loop <= 0:
                break

        fig = plt.figure()
        fig.add_subplot(2, 1, 1)
        bins_lat = np.linspace(start=variances_lat.min(), stop=variances_lat.max(), num=10)
        histogram_lat = np.histogram(variances_lat, bins_lat)
        bins_lat = 0.5 * (bins_lat[1:] + bins_lat[:-1])
        plt.plot(bins_lat, histogram_lat[0])
        fig.add_subplot(2, 1, 2)
        bins_lon = np.linspace(start=variances_lon.min(), stop=variances_lon.max(), num=10)
        histogram_lon = np.histogram(variances_lat, bins_lon)
        bins_lon = 0.5 * (bins_lon[1:] + bins_lon[:-1])
        plt.plot(bins_lon, histogram_lon[0])
        plt.show()

    def space_revelance_analysis(self, loop=20, period=20):
        """
        @function: analyze the spatial relevance of ADS-B
        @author: Tengyao Li
        @date: 2018/09/12
        
        @:param loop: limit the amount of flights
        @:param period: limit the time cycles
        :return: none 
        """

        neighbor_deviation = np.zeros(loop)  # record the change of density for each flight
        neighbor_density = np.zeros((loop, period))  # record the density for specific flight and time

        for icao in self.df.icao24.unique():

            df_cruise = self.df.loc[self.df.icao24 == icao]  # get the current flight route

            pieces = 1  # the record point
            separation = 10  # time separation (time:  pieces*seperation*10)
            while pieces <= period:

                threshold = 10  # the communication distance
                amount = 0  # the neighbor flight

                if pieces * separation >= df_cruise.shape[0]:
                    break

                df_density = self.df.loc[self.df.time == df_cruise.time.iloc[pieces * separation]]
                cur_lat = df_density.loc[df_density.icao24 == icao].lat.iloc[0]
                cur_lon = df_density.loc[df_density.icao24 == icao].lon.iloc[0]
                for i in np.arange(df_density.shape[0]):
                    # calculate the distance (here, the distance should be replaced)
                    deviation = np.vstack((np.array([df_density.lat.iloc[i], df_density.lon.iloc[i]]),
                                           np.array([cur_lat, cur_lon])))
                    distance = pdist(deviation)

                    if np.isnan(distance):
                        continue

                    if distance < threshold:
                        amount += 1

                neighbor_density[loop - 1, pieces - 1] = amount

                pieces += 1

            # fig = plt.figure()
            # plt.plot(np.linspace(start=100, stop=period * separation * 10, num=period), neighbor_density[loop-1, :])

            neighbor_deviation[loop - 1] = np.mean(neighbor_density[loop - 1, 1:] - neighbor_density[loop - 1, :-1])

            # loop control
            # limit the amount of flights
            loop -= 1
            if loop <= 0:
                break

        bins = np.linspace(start=neighbor_deviation.min(), stop=neighbor_deviation.max(), num=5)
        histogram_deviation = np.histogram(neighbor_deviation, bins)
        bins = 0.5 * (bins[1:] + bins[:-1])
        plt.plot(bins, histogram_deviation[0])

        plt.show()

    def characteristic_analysis(self, loop=5):
        """
        @function: analyze the characteristic of ADS-B data
        @author: Tengyao Li
        @date: 2018/09/13
        
        @:param: limit the flight amount
        :return: none 
        """
        for icao in self.df.icao24.unique():

            df_cruise = self.df.loc[self.df.icao24 == icao]  # get the current flight route

            # plot the relative attribute to improve analysis
            fig = plt.figure()
            fig.add_subplot(2, 2, 1)
            plt.plot(df_cruise.time, df_cruise.velocity, '-')
            plt.xlabel("time")
            plt.xticks([])
            plt.ylabel("velocity")
            plt.title("(a)")
            fig.add_subplot(2, 2, 2)
            plt.plot(df_cruise.time, df_cruise.heading, '-')
            plt.xlabel("time")
            plt.xticks([])
            plt.ylabel('heading')
            plt.title("(b)")
            fig.add_subplot(2, 2, 3)
            plt.plot(df_cruise.time, df_cruise.geoaltitude, '-')
            plt.xlabel("time")
            plt.xticks([])
            plt.ylabel('geographical altitude')
            plt.title("(c)")
            fig.add_subplot(2, 2, 4)
            plt.plot(df_cruise.time, df_cruise.vertrate, '-')
            plt.xlabel("time")
            plt.xticks([])
            plt.ylabel('vertical rate')
            plt.title("(d)")
            # fig.suptitle("Characteristic Analysis for flight - %s" % df_cruise.callsign.iloc[0])

            # loop control
            # limit the amount of flights
            loop -= 1
            if loop <= 0:
                break

        plt.show()


### scripts here!
analyzor = data_analysis()
# analyzor.time_relevance_analysis()
# analyzor.space_revelance_analysis(5, 5)
analyzor.characteristic_analysis()
