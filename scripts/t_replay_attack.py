"""
@function: scripts the replay attack
@author: Tengyao Li
@date: 2018/09/30
@status: developing
@code-type: testing script
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from attack_pattern import replay_attack

# scripts the parent class: attack_pattern [1 functions]
# status: success
test = replay_attack.replay_attack(2019, 12, 23, 0, 0)
# print(scripts.get_attacked_targets())
# print('The percent of attacked flights is:\t %f' % scripts.get_attacked_percent())
original_data = test.get_original_df()

# scripts attack pattern: time delay attack
# status: testing
def test_time_replay_deviation():
    startTime = time.time()
    attacked_df0 = test.time_replay_attack(300)
    endTime = time.time()
    print('The running time for [time replay attack] is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():

        base_time = original_data.loc[original_data.icao24 == attacked_icao[0],'time'].iloc[0]

        fig = plt.figure()

        ax = Axes3D(fig)

        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].time - base_time,
                c='r', marker='*')

        ax.plot(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].time - base_time,
                c='b', marker='o')

        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('time')

        # plt.title('The replay attack [time replay deviation] for %s' % attacked_icao)

    plt.show()

### testing execution
test_time_replay_deviation() # success
