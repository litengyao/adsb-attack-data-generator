"""
@function: the base class for concrete attack classes
@author: Tengyao Li
@date: 2018/09/12
@update: 2019/04/30
@status: developing
"""

from data_io import read_adsb
from attack_choice import attacked_flight


class attack:
    """
    @function: integrate the common operations for different attacks
    @author: Tengyao Li
    @date: 2018/09/12    
    """

    def __init__(self, year=2019, month=12, day=23, start_hour=0, end_hour=0):
        """
        @function: get the original dataset
        @author: Tengyao Li
        @date: 2018/09/12

        :param year: year
        :param month: month
        :param day: day
        :param start_hour: the beginning hour
        :param end_hour: the end hour(included)
        :return: none
        """

        reader = read_adsb.reader(year=year, month=month, day=day)
        self.origin_df = reader.get_continious_data(start_hour=start_hour, end_hour=end_hour)

        self.set_attacked_targets(self.origin_df)

    def get_original_df(self):
        """
        @function: get the original normal data
        @author: Tengyao Li
        @date: 2018/09/29
        :return: the original normal data
        """

        return self.origin_df

    def get_attacked_targets(self):
        """
        @function: get the attacked flight icao set
        @author: Tengyao Li
        @date: 2018/09/12

        :return: the attacked target flight icao set 
        """

        return self.attacked_targets

    def get_attacked_percent(self):
        """
        @function: get the percentage of attacked flights
        @author: Tengyao Li
        @date: 2018/09/14
        
        :return: the percentage of attacked flights
        """

        return self.percent

    def set_original_df(self, selected_df):
        """
        reset the original dataset
        :param selected_df: the newer dataset
        :return: none
        """
        self.origin_df = selected_df

    def set_attacked_targets(self, origin_df):
        # generate the attacked targets
        self.percent = 0.0005  # the attacked flight percentage
        generator = attacked_flight.attacked_flight(origin_df)
        self.attacked_targets = generator.choose_attack_flight('random', self.percent)
