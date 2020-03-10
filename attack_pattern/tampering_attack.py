"""
@function: design and create attack data under tampering attack
@author: Tengyao Li
@date: 2018/09/12
@update: 2018/09/14
@status: developing
"""

import numpy as np
from attack_pattern import attack


class tampering_attack(attack.attack):
    """
    @function: reconstruct the influence on ADS-B with tampering attack_pattern
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

    def inject_random_deviation(self, *args):
        """
        @function: inject random deviation to the original data
        @author: Tengyao Li
        @date: 2018/09/12
                
        :param args: the attributes to be tampered (dtype: string)
        :return: the attacked dataset 
        """

        attacked_df = self.origin_df.copy()

        # core operations
        for icao in self.attacked_targets:

            for i in np.arange(len(args)):
                # construct the random deviation
                attack_impact_percentage = 0.035  # the deviation scope (the strength of attack_pattern)
                rand = (np.random.random(
                    attacked_df[attacked_df.icao24 == icao[0]][args[i]].shape) * (
                            attacked_df[attacked_df.icao24 == icao[0]][args[i]].max() - attacked_df[
                                attacked_df.icao24 == icao[0]][args[i]].min())) * attack_impact_percentage

                attacked_df.loc[attacked_df.icao24 == icao[0], args[i]] += rand

        return attacked_df

    def inject_constant_deviation(self, deviation, *args):
        """
        @function: inject constant deviation to the original data
        @author: Tengyao Li
        @date: 2018/09/13
        
        :param deviation: the constant deviation list
        :param args: the attributes to be tampered (dtype: string)
        :return: the attacked dataset
        """

        # keep the relevant relationship on amount
        if len(deviation) != len(args):
            return None

        attacked_df = self.origin_df.copy()

        # core operations
        for icao in self.attacked_targets:
            for i in np.arange(len(args)):
                attacked_df.loc[attacked_df.icao24 == icao[0], args[i]] += deviation[i]

        return attacked_df

    def inject_increase_deviation(self, initial_deviation, increase_ratio, *args):
        """
        @function: inject initial deviation and make the deviation increased with the constant ratio
        @author: Tengyao Li
        @date: 2018/09/13
        
        :param initial_deviation: the initial deviation
        :param increase_ratio: the ratio to increase (should be small enough)
        :param args: the attributes to be tampered(dtype: string)
        :return: the attacked dataset
        """

        # keep the relevant relationship on amount
        if len(initial_deviation) != len(args):
            return None

        if len(initial_deviation) < len(increase_ratio):
            return None

        attacked_df = self.origin_df.copy()

        # core operations
        for icao in self.attacked_targets:
            cur_deviation = initial_deviation
            for t in np.arange(attacked_df[attacked_df.icao24 == icao[0]].shape[0]):
                for i in np.arange(len(args)):
                    attacked_df.loc[attacked_df.icao24 == icao[0], args[i]] += cur_deviation[i]
                    cur_deviation[i] = cur_deviation[i] * (1 + increase_ratio[i])

        return attacked_df

    def inject_changeable_deviation(self, deviation, *args):
        """
        @function: inject deviation that is fluctuated with time
        @author: Tengyao Li
        @date: 2018/09/14
        
        :param deviation: the constant deviation list (basic deviation) 
        :param args: the attributes to be tampered(dtype: string)
        :return:  the attacked dataset
        """

        # keep the relevant relationship on amount
        if len(deviation) != len(args):
            return None

        attacked_df = self.origin_df.copy()
        # core operations
        for icao in self.attacked_targets:
            elapse_time = 0
            for t in np.arange(attacked_df[attacked_df.icao24==icao[0]].time.shape[0]):
                for i in np.arange(len(args)):
                    attacked_df.loc[attacked_df.icao24 == icao[0], args[i]] += deviation[i] * np.log(1 + elapse_time)

                elapse_time += 1

        return attacked_df

    def inject_zoom_deviation(self, zoom_factor, *args):
        """
        @function: multiply zoom factor with variable itself
        @author: Tengyao Li
        @date: 2018/09/14 
        
        :param args: the attributes to be tampered(dtype: string) 
        :return: the attacked dataset
        """

        attacked_df = self.origin_df.copy()
        # core operations
        for icao in self.attacked_targets:
            for i in np.arange(len(args)):
                attacked_df.loc[attacked_df.icao24 == icao[0], args[i]] *= zoom_factor[i]

        return attacked_df

    def inject_nonlinear_deviation(self, *args):
        """
        @function: inject nonlinear deviations
        @author: Tengyao Li
        @date: 2018/09/14
        
        @tips: this method will be extended in the future
        
        :param args: the attributes to be tampered(dtype: string) 
        :return: the attacked dataset
        """

        attacked_df = self.origin_df.copy()
        # core operations
        for icao in self.attacked_targets:
            for i in np.arange(len(args)):
                attacked_df.loc[attacked_df.icao24 == icao[0], args[i]] = np.power(
                    attacked_df.loc[attacked_df.icao24 == icao[0], args[i]], 2)

        return attacked_df
