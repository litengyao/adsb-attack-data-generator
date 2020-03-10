"""
@function: design and create attack data under ghost attack
@author: Tengyao Li
@date: 2018/09/12
@update: 2018/09/14
@status: developing
"""

from attack_pattern import attack
import numpy as np
import pandas as pd


class ghost_attack(attack.attack):
    """
    @function: reconstruct the influence on ADS-B with ghost attack_pattern. 
    Considering the special characteristic for this attack_pattern, we only use the attacked_targets attribute partly. 
    @author: Tengyao Li
    @date: 2018/09/14
    """

    def __init__(self, year=2017, month=11, day=20, start_hour=0, end_hour=0):
        """
        @function: initialize the parent class __init__()
        @author: Tengyao Li
        @date: 2018/09/29        
        """
        super().__init__(year, month, day, start_hour, end_hour)

    def copy_ghost(self, ghost_icao, ghost_lat, ghost_lon):
        """
        @function: copy the neighbor flight as ghost(only for single ghost)
        @author: Tengyao Li
        @date: 2018/09/14
        
        :param ghost_icao: the ghost icao
        :param ghost_lat: ghost flight latitude
        :param ghost_lon: ghost flight longitude
        :return: the attacked dataset, the ghost flight
        """

        attacked_df = self.origin_df.copy()

        threshold = 1000  # the neighbor standard radius
        for i in np.arange(attacked_df.shape[0]):
            # the distance calculation will be improved in the future
            # Please don't use the scheme: attacked_df[i].lat, it doesn't work
            if np.sqrt((attacked_df.lat[i] - ghost_lat) ** 2 + (attacked_df.lon[i] - ghost_lon) ** 2) < threshold:
                cur_df = attacked_df[attacked_df.icao24 == attacked_df.icao24[i]].copy()  # bug fixed: deep copy
                cur_df.icao24 = ghost_icao
                cur_df.lat = cur_df.lat + (ghost_lat - attacked_df.lat[i])
                cur_df.lon = cur_df.lon + (ghost_lon - attacked_df.lon[i])
                attacked_df = pd.concat([attacked_df, cur_df])  # bug fixed: must be a list to put into concat
                break

        return attacked_df, cur_df

    def create_ghost(self, ghost_icao):
        """
        @function: create the ghost with IMM
        @author: Tengyao Li
        @date: 2018/09/14
        
        :param ghost_icao: the ghost icao
        :return: the attacked dataset
        """

        attacked_df = self.origin_df.copy()

        # we just use the message template instead of content
        for icao in self.attacked_targets:
            cur_df = attacked_df[attacked_df.icao24 == icao[0]].copy()
            break

        cur_df.loc[:, 'icao24'] = ghost_icao

        a_lat = 0.3
        v0_lat = 0.02
        a_lon = 0.26
        v0_lon = 0.02

        for i in np.arange(cur_df.lat.shape[0] - 1):
            cur_df.iat[i + 1, 2] = cur_df.iat[i, 2] + 50 * a_lat + 10 * v0_lat  # bug fixed: index 2: lat
            cur_df.iat[i + 1, 3] = cur_df.iat[i, 3] + 50 * a_lon + 10 * v0_lon  # bug fixed: index 3: lon

        attacked_df = pd.concat([attacked_df, cur_df])  # bug fixed: it is in demand of lists to put into concat

        return attacked_df, cur_df

    def random_ghost(self, ghost_icao):
        """
        @function: create the ghost with random data
        @author: Tengyao Li
        @date: 2018/09/14
        
        :param ghost_icao: the ghost icao
        :return: the attacked dataset
        """

        attacked_df = self.origin_df.copy()

        # we just use the message template instead of content
        cur_df = attacked_df[attacked_df.icao24 == self.attacked_targets[0][0]].copy()

        cur_df.icao24 = ghost_icao

        rand = np.random.random((cur_df.lat.shape[0], 3))
        np.add(cur_df.lat, rand[:, 0])
        np.add(cur_df.lon, rand[:, 1])
        np.add(cur_df.baroaltitude, rand[:, 2])

        pd.concat([attacked_df, cur_df])

        return attacked_df, cur_df
