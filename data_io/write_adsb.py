"""
@function: write the dataset to outside file
@author: Tengyao Li
@date: 2018/09/12
"""
import pandas as pd

from data_io import read_adsb


class writer:
    """
    @function: push the attack_pattern dataset to outside file
    @author: Tengyao Li
    @date: 2018/09/12
    """

    def __int__(self):
        pass

    def test(self):
        reader = read_adsb.reader()
        origin_df = reader.get_continious_data(start_hour=0, end_hour=0)
        origin_df[origin_df.icao24 == '49d3fa'].to_csv('output/output.csv')

### scripts here!
# tt = writer()
# tt.scripts()
