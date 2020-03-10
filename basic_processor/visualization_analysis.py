"""
@function: analyzing data relying on visualization
@author: Tengyao Li
@date: 2018/09/11
@update: 2018/09/12
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import time

from util.parameter import DATA_INPUT_PATH

# merge dataset for different hours
hour_limitation = 1  # limit the amount of dataset to merge
df = pd.DataFrame()
for hour in range(hour_limitation):
    if hour < 10:
        dfx = pd.read_csv(DATA_INPUT_PATH + '/states_2019-12-23-0%i.csv' % hour)
    else:
        dfx = pd.read_csv(DATA_INPUT_PATH + '/states_2019-12-23-%i.csv' % hour)

    dfx.time = dfx.time.apply(lambda x: time.strftime("%H:%M:%S", time.localtime(x)))

    df = df.append(dfx, ignore_index=True)

loop = 1  # limit the amount of flights
highest_altitude = df.baroaltitude.max()  # used to limit the axis range
for icao in df.icao24.unique():

    df_cruise = df.loc[df.icao24 == icao]  # get the current flight route

    # plot the flight track ( the point to get off is marked with circle)
    fig0 = plt.figure()
    fig0.add_subplot(1, 1, 1)
    ax = Axes3D(fig0)
    ax.plot(df_cruise.lat, df_cruise.lon, df_cruise.baroaltitude)
    ax.scatter(df_cruise.iloc[0].lat, df_cruise.iloc[0].lon, df_cruise.iloc[0].baroaltitude, c='r', marker='>')
    ax.set_xlabel("latitude")
    ax.set_ylabel("longitude")
    ax.set_zlabel("altitude")
    ax.set_zlim(0, highest_altitude)
    # plt.title("the track of flight: %s" % df_cruise.callsign.iloc[0])
    # fig0.savefig('%s-track.eps' % df_cruise.callsign.iloc[0], format='eps')

    # plot the relative attribute to improve analysis
    fig1 = plt.figure()
    fig1.add_subplot(2, 2, 1)
    plt.plot(df_cruise.time, df_cruise.velocity, '-')
    plt.xlabel("time")
    plt.ylabel("velocity")
    plt.title("(a)")
    fig1.add_subplot(2, 2, 2)
    plt.plot(df_cruise.time, df_cruise.heading, '-')
    plt.xlabel("time")
    plt.ylabel('heading')
    plt.title("(b)")
    fig1.add_subplot(2, 2, 3)
    plt.plot(df_cruise.time, df_cruise.geoaltitude, '-')
    plt.xlabel("time")
    plt.ylabel('geoaltitude')
    plt.title("(c)")
    fig1.add_subplot(2, 2, 4)
    plt.plot(df_cruise.time, df_cruise.vertrate, '-')
    plt.xlabel("time")
    plt.ylabel('vertrate')
    plt.title("(d)")
    # fig1.suptitle("Characteristic Analysis for flight - %s" % df_cruise.callsign.iloc[0])
    # fig1.savefig('%s-characteristics.eps' % df_cruise.callsign.iloc[0], format='eps')

    # # plot the neighbor airspace density
    # time_range = 1  # control the cycle amount to analyze
    # for i in range(time_range):
    #     fig2 = plt.figure()
    #     count = 1
    #     for t in df_cruise.time[20 * i:20 * (i + 1)]:
    #         fig2.add_subplot(4, 5, count)
    #
    #         df_density = df.loc[df.time == t]
    #         plt.scatter(df_density.lat, df_density.lon)
    #         plt.plot(df_cruise.iloc[0].lat, df_cruise.iloc[0].lon, 'r+')
    #         plt.xlabel("latitude")
    #         plt.xlim(df_cruise.iloc[0].lat - 5, df_cruise.iloc[0].lat + 5)
    #         plt.ylabel("longitude")
    #         plt.ylim(df_cruise.iloc[0].lon - 5, df_cruise.iloc[0].lon + 5)
    #         plt.title("(%s)" % count)
    #         count += 1
    #     fig2.suptitle("spatial relevance analysis for flight - %s" % df_cruise.callsign.iloc[0])
    #     fig2.savefig('%s-density-%i-cycle.eps' % (df_cruise.callsign.iloc[0], i),format='eps',dpi=1000)

    pieces = 1  # the record point
    separation = 10  # time separation (time:  pieces*seperation*10)
    fig2 = plt.figure()
    # plt.subplots_adjust(wspace=1, hspace=.3)
    while pieces < 21:
        df_density = df.loc[df.time == df_cruise.time.iloc[pieces * separation]]

        fig2.add_subplot(4, 5, pieces)

        plt.scatter(df_density.lat, df_density.lon)

        plt.plot(df_cruise.iloc[0].lat, df_cruise.iloc[0].lon, 'r+')
        if pieces > 14:
            plt.xlabel("latitude")
        plt.xlim(df_cruise.iloc[0].lat - 5, df_cruise.iloc[0].lat + 5)

        plt.ylabel("longitude")
        plt.ylim(df_cruise.iloc[0].lon - 5, df_cruise.iloc[0].lon + 5)
        plt.title("(%s)" % pieces)

        pieces += 1

    # fig2.suptitle("spatial relevance analysis for flight - %s" % df_cruise.callsign.iloc[0])
    # fig2.savefig('%s-density.eps' % (df_cruise.callsign.iloc[0]), format='eps')

    # loop control
    # limit the amount of flights
    loop -= 1
    if loop <= 0:
        break

plt.show()
