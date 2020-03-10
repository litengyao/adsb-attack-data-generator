"""
@function: design and create attack data under dos attack
@author: Tengyao Li
@date: 2018/09/12
@status: developing
"""

from attack_pattern import attack
import numpy as np


class dos_attack(attack.attack):
    """
    @function: reconstruct the influence on ADS-B with dos attack_pattern
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

    def period_dos_attack(self, start_timestamp, end_timestamp):
        """
        @function: attack_pattern implementation: attack_pattern for specific period
        @author: Tengyao Li
        @date: 2018/09/12
        
        :return: attacked dataset
        """

        attacked_df = self.origin_df.copy()
        for icao in self.attacked_targets:
            cur_df = self.origin_df.loc[self.origin_df.icao24 == icao[0]].copy()

            # the core operations
            cur_df.loc[(cur_df.time > start_timestamp) & (cur_df.time < end_timestamp)] = np.nan

            # construct the attacked data
            attacked_df[icao[0] == attacked_df.icao24] = cur_df

        return attacked_df

    def whole_dos_attack(self):
        """
        @function: delete the corresponding message(also called as delete attack_pattern on ADS-B data)
        @author: Tengyao Li
        @date: 2018/09/12
                
        :return: the attacked dataset 
        """

        attacked_df = self.origin_df.copy()

        # core operations
        # we just change the value to NaN
        for icao in self.attacked_targets:
            attacked_df.loc[
                attacked_df.icao24 == icao[0], ['lat', 'lon', 'velocity', 'heading', 'vertrate', 'baroaltitude',
                                             'geoaltitude']] = np.nan

        return attacked_df

    def cycle_dos_attack(self, time_span, last_time):
        """
        @function: delete the message for specific time period and implement the attack_pattern for several cycles
        @author: Tengyao Li
        @date: 2018/09/12
        
        @tips: this method will be extended in the future
        
        :param time_span: the time period for normal status
        :param last_time: the time period for attacking operations
        :return: the attacked data
        """

        attacked_df = self.origin_df.copy()

        for icao in self.attacked_targets:
            cur_df = attacked_df.loc[attacked_df.icao24 == icao[0]].copy()
            count = 0
            attacking = False
            for t in cur_df.time:
                count += 1

                if attacking is False and count == time_span:
                    attacking = True
                    count = 0

                if attacking:

                    if count == last_time:
                        count = 0
                        attacking = False

                    attacked_df.loc[
                        (attacked_df.time == t) & (attacked_df.icao24 == icao[0]), ['lat', 'lon', 'velocity', 'heading',
                                                                               'vertrate', 'baroaltitude',
                                                                               'geoaltitude']] = np.nan

        return attacked_df


