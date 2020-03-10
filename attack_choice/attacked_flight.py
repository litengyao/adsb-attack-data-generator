"""
@function: choose the attacked flights
@author: Tengyao Li
@date: 2018/09/12
@status: developing
"""

import numpy as np


class attacked_flight:
    """
    @function: get the attacked icao set
    @author: Tengyao Li
    @date: 2018/09/12
    """

    def __init__(self, origin_df):
        """
        @function: initialize the origin dataset
        @author: Tengyao Li
        @date: 2018/09/12
        """
        self.origin_df = origin_df

    def choose_attack_flight(self, rule='random', *args, **params):
        """
        @function: choose the attack_pattern destination
        @author: Tengyao Li
        @date: 2018/09/12

        @:param rule: the rule to select attack_pattern targets
        @:param args: the changeable parameters
        @:param params: the key parameters as dict type
        :return: the attack_pattern icao set (string list)
        """

        if rule == 'random':
            """
            @illustration: choose the attack_pattern target randomly
            @args:
            # 1st(percentage): float / the percentage of attack_pattern targets, 
            control the attack_pattern flight amount in the whole dataset            
            """

            percentage = args[0]
            icaoset = self.origin_df.icao24.unique()
            amount = int(np.floor(percentage * icaoset.shape[0]))
            rand = np.random.random_integers(0, icaoset.shape[0], size=(amount, 1))

            attacked_icao = []  # Issue: the redundancy of icao index ( should be improved later)
            for i in rand:
                attacked_icao.append(icaoset[i])

            return attacked_icao

        elif rule == 'area':
            """
            @illustration: choose the attack_pattern target from specific areas
            @args:
            # timestamp: the timestamp of choice
            @params:            
            # start_lat: the beginning latitude
            # start_lon: the beginning longitude
            # end_lat: the end boundary of latitude
            # end_lon: the end boundary of longitude
            """
            cur_df = self.origin_df.loc[self.origin_df.time == args[0]]

            attacked_icao = []

            for icao in cur_df.icao24:
                cur_record = cur_df.loc[cur_df.icao24 == icao]
                if cur_record.lat.iloc[0] >= params['start_lat'] \
                        and cur_record.lat.iloc[0] <= params['end_lat'] \
                        and cur_record.lon.iloc[0] >= params['start_lat'] \
                        and cur_record.lon.iloc[0] <= params['end_lon']:
                    attacked_icao.append(icao)

            return attacked_icao

        elif rule == 'list':
            """
            @illustration: choose the attack_pattern target for specific targets list
            @args:
            # the icao24 attributes of target flights
            """
            attacked_icao = []
            for icao in args:
                attacked_icao.append(icao)

            return attacked_icao
        else:
            pass
