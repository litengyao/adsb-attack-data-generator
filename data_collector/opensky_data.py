"""
Obtain the batch data from http://www.opensky-network.org
功能：  从http://www.opensky-network.org获取批量ADS-B数据
作者：  李腾耀
日期：  2017/11/27
更新：  2018/09/10

"""

from urllib import request

import os
import time
import csv

from opensky_api import OpenSkyApi


class OpenskyData:
    """
    功能：  实现对opensky-network.org数据的获取处理和分析
    日期：  2017-11-27
    """

    def __init__(self, path):
        """
        功能：  初始化opensky-network账户密码
        日期：2017-11-27
        """
        self.userName = "ltyleader"
        self.password = ""  # 代码共享时，密码已删除
        self.path = path

    def callback_receiveData(self, downloadedDataBlock, blockSize, remoteFileSize):
        """
        功能：显示文件的下载进度
        日期：2017-11-27
        :param downloadedDataBlock:  已经下载的数据块 
        :param blockSize: 数据块的大小
        :param remoteFileSize: 远程文件的大小
        :return:   无
        """

        #  计算下载百分比
        progress = 100.0 * downloadedDataBlock * blockSize / remoteFileSize
        if progress > 100:
            progress = 100

        # 输出当前文件下载进度（为了避免频繁输出，所以限定输出）
        if (progress - int(progress) < 1e-7):
            print("{0:.2f}%".format(progress))

    def receiveData(self, day, hour="00", format="csv"):
        """
        功能：  针对特定时间点的数据进行获取
        日期：  2017-11-27
        :param day:   待获取的数据所在日期；需要满足如下的格式:2017-11-20
        :param hour:   待获取的数据对应的时间；需要满足如下的格式：00 01 ... 22 23
        :param format:  待获取的数据对应的格式；可选项包括：csv avro json
        :return: 无
        """

        # 格式检查
        if len(day.split("-")) != 3:  # 日期检查
            print("日期格式错误，请调整为示例2017-11-20满足的格式")
            return
        if int(hour) > 23 or int(hour) < 0 or len(hour) != 2:  # 时间检查
            print("时间格式错误，请调整为示例00 23满足的格式")
            return
        if format != "csv" and format != "avro" and format != "json":  # 数据格式检查
            print("opensky-network.org数据站点中不包含您所需要的格式")
            return

        # 数据传输基路径：数据站点为opensky-network.org的数据仓库，本地存储默认为当前路径
        webBasePath = "https://opensky-network.org/datasets/states/"
        localBasePath = self.path

        # webPath拼接
        filename = "states_" + day + "-" + hour + "." + format + ".tar"
        webPath = os.path.join(webBasePath, day, hour, filename).replace("\\", "/")
        localPath = os.path.join(localBasePath, filename)

        # 获取数据
        urllib = request.urlretrieve(webPath, localPath, self.callback_receiveData)

    def batchReceiveData(self, date, start_hour=0, stop_hour=24):
        """
        功能：批量获取对应日期所有数据（使用默认csv格式）
        :param date: 数据日期（字符串）
        :param start_hour: 数据的起始时间点
        :param stop_hour: 数据的结束时间点（不包含）
        :return: 无
        """

        for h in range(start_hour, stop_hour):
            hour = 0
            if h < 10:
                hour = "0" + str(h)
            else:
                hour = str(h)

            self.receiveData(date, hour)
            print("{0:s}:{1:s}:00:00 数据获取完毕".format(date, hour))

    def receiveRealTimeData(self, path="F:/research/DATA/opensky/", filename="data.csv", period=180):
        """
        功能：  通过实时API获取数据
        日期：  2017-11-27
        :param path:  基本路径
        :param filename: 文件名称
        :param period:  运行时长设置 
        :return: 无
        """

        #  创建输出文件
        timestamp = int(time.time())
        output_file = open(os.path.join(path, str(timestamp) + "-" + filename), 'a', newline='')
        writer = csv.writer(output_file)

        while period > 0:
            #  获取实时数据
            api = OpenSkyApi(self.userName, self.password) # 使用用户名和密码登陆获得授权
            # api = OpenSkyApi()
            states = api.get_states()

            timestamp = int(time.time())

            """
            说明：  这是State_Vector的格式字段说明
            icao24 - ICAO24 address of the transmitter in hex string representation.
            callsign - callsign of the vehicle. Can be None if no callsign has been received.
            origin_country - inferred through the ICAO24 address
            time_position - seconds since epoch of last position report. Can be None if there was no position report received by OpenSky within 15s before.
            last_contact - seconds since epoch of last received message from this transponder
            longitude - in ellipsoidal coordinates (WGS-84) and degrees. Can be None
            latitude - in ellipsoidal coordinates (WGS-84) and degrees. Can be None
            geo_altitude - geometric altitude in meters. Can be None
            on_ground - true if aircraft is on ground (sends ADS-B surface position reports).
            velocity - over ground in m/s. Can be None if information not present
            heading - in decimal degrees (0 is north). Can be None if information not present.
            vertical_rate - in m/s, incline is positive, decline negative. Can be None if information not present.
            sensors - serial numbers of sensors which received messages from the vehicle within the validity period of this state vector. Can be None if no filtering for sensor has been requested.
            baro_altitude - barometric altitude in meters. Can be None
            squawk - transponder code aka Squawk. Can be None
            spi - special purpose indicator
            position_source - origin of this state’s position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT
           """

            # 输出数据到CSV格式文件中
            writer.writerow(
                ["time", "icao24", "lat", "lon", "velocity", "heading", "vertrate", "callsign", "onground", "alert",
                 "spi",
                 "squawk", "baroaltitude", "geoaltitude", "lastposupdate", "lastcontact", "sensors", "position_source"])
            for s in states.states:
                writer.writerow(
                    [timestamp, s.icao24, s.latitude, s.longitude, s.velocity, s.heading, s.vertical_rate, s.callsign,
                     s.on_ground, "", s.spi, s.squawk, s.baro_altitude, s.geo_altitude, s.time_position, s.last_contact,
                     s.sensors, s.position_source])

            print("时间戳{0:d}： 已写入当前数据".format(timestamp))

            time.sleep(10)

            period -= 10

        print("数据下载写入完成")

        output_file.close()
