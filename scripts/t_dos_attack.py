"""
@function: scripts the dos attack
@author: Tengyao Li
@date: 2018/12/03
@status: developing
@code-type: testing script
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from attack_pattern import dos_attack

test = dos_attack.dos_attack(2019, 12, 23, 0, 0)

original_data = test.get_original_df()


# scripts attack pattern: dos attack
# status: testing
def test_period_dos_attack():
    startTime = time.time()
    attacked_df0 = test.period_dos_attack(1511136550, 1511136910)
    endTime = time.time()
    print('The running time for [dos attack] is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()

        ax = Axes3D(fig)

        ax.scatter(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')

        ax.scatter(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')

        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('baroaltitude')

        # plt.title('The dos attack [period dos attack] for %s' % attacked_icao)

    plt.show()

def test_whole_dos_attack():
    startTime = time.time()
    attacked_df0 = test.whole_dos_attack()
    endTime = time.time()
    print('The running time for [dos attack] is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()

        ax = Axes3D(fig)

        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')

        ax.scatter(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')

        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('baroaltitude')

        # plt.title('The dos attack [whole dos attack] for %s' % attacked_icao)

    plt.show()

def test_cycle_dos_attack():
    startTime = time.time()
    attacked_df0 = test.cycle_dos_attack(50, 30)
    endTime = time.time()
    print('The running time for [dos attack] is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()

        ax = Axes3D(fig)

        ax.scatter(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')

        ax.scatter(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')

        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('baroaltitude')

        # plt.title('The dos attack [whole dos attack] for %s' % attacked_icao)

    plt.show()

### testing execution
# test_period_dos_attack()  # success
# test_whole_dos_attack()
test_cycle_dos_attack()
