"""
@function: design and create attack data under replay attack
@author: Tengyao Li
@date: 2018/09/12
@status: developing
"""

import numpy as np

from attack_pattern import attack
from data_io import read_adsb
from attack_choice import attacked_flight


class replay_attack(attack.attack):
    """
    @function: reconstruct the influence on ADS-B with replay attack_pattern
    @author: Tengyao Li
    @date: 2018/09/12
    """

    def __init__(self, year=2017, month=11, day=20, start_hour=0, end_hour=0):
        """
        @function: initialize the parent class __init__()
        @author: Tengyao Li
        @date: 2018/09/29        
        """
        super().__init__(year, month, day, start_hour, end_hour)

    def time_replay_attack(self, time_span):
        """
        @function: the classic replay attack_pattern
        @author: Tengyao Li
        @date: 2018/09/12
        @status: waiting to be updated to realize the actual time replay attack
        
        :param time_span: the time to delay (or the time to replay) [per record/10s]
        :return: the attacked dataset
        """

        attacked_df = self.origin_df.copy()
        for icao in self.attacked_targets:

            index_deviation = int(time_span / 10)
            length = self.origin_df.loc[attacked_df.icao24 == icao[0]].shape[0]-index_deviation
            temp_df = attacked_df.loc[attacked_df.icao24 == icao[0]].copy()
            for i in np.arange(length):
                temp_df.iloc[length - 1 + index_deviation - i] = temp_df.iloc[length - 1 - i] # bug fixing

            for i in np.arange(index_deviation):
                temp_df.iloc[i] = temp_df.iloc[index_deviation]

            attacked_df.loc[attacked_df.icao24 == icao[0],'lat'] = temp_df.lat
            attacked_df.loc[attacked_df.icao24 == icao[0],'lon'] = temp_df.lon
            attacked_df.loc[attacked_df.icao24 == icao[0],'baroaltitude'] = temp_df.baroaltitude

        return attacked_df
