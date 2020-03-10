"""
@function: scripts the tampering attack
@author: Tengyao Li
@date: 2018/09/29
@update: 2018/09/30
@status: developing
@code-type: testing script
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from attack_pattern import tampering_attack

# scripts the parent class: attack_pattern [6 functions]
# status: success
test = tampering_attack.tampering_attack(2019, 12, 23, 0, 0)
# print(scripts.get_attacked_targets())
# print('The percent of attacked flights is:\t %f' % scripts.get_attacked_percent())
original_data = test.get_original_df()


# scripts attack pattern: inject_random_deviation
# status: success
def test_inject_random_deviation():
    attacked_df0 = test.inject_random_deviation('lat', 'lon', 'baroaltitude')
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')
        ax.plot(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('altitude')
        # plt.title('The tampering attack [inject random deviation] for %s' % attacked_icao)

    plt.show()


# scripts attack pattern: inject_constant_deviation
# status: success
def test_inject_constant_deviation():
    attacked_df0 = test.inject_constant_deviation([2.5, 2.5, 2000], 'lat', 'lon', 'baroaltitude')
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')
        ax.plot(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('altitude')
        # plt.title('The tampering attack [inject constant deviation] for %s' % attacked_icao)

    plt.show()


# scripts attack pattern: inject_increase_deviation
# status: success -- waiting for further verification
def test_inject_increase_deviation():
    startTime = time.time()
    attacked_df0 = test.inject_increase_deviation([0.0005, 0.0005, 0.01], [0.0002, 0.0002, 0.000005], 'lat', 'lon',
                                                  'baroaltitude')
    endTime = time.time()
    print('The running time is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')
        ax.plot(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('altitude')
        # plt.title('The tampering attack [inject increased deviation] for %s' % attacked_icao)

    plt.show()


# scripts attack pattern: inject_changeable_deviation
# status: success
def test_inject_changeable_deviation():
    startTime = time.time()
    attacked_df0 = test.inject_changeable_deviation([0.25, 0.25, 200], 'lat', 'lon', 'baroaltitude')
    endTime = time.time()
    print('The running time for [inject changeable deviation attack] is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')
        ax.plot(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('altitude')
        # plt.title('The tampering attack [inject changeable deviation] for %s' % attacked_icao)

    plt.show()


# scripts attack pattern: inject_zoom_deviation
# status: success
def test_inject_zoom_deviation():
    startTime = time.time()
    attacked_df0 = test.inject_zoom_deviation([2.0, 3.0, 1.5], 'lat', 'lon', 'baroaltitude')
    endTime = time.time()
    print('The running time for [inject zoom deviation attack] is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')
        ax.plot(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('altitude')
        # plt.title('The tampering attack [inject zoom deviation] for %s' % attacked_icao)

    plt.show()


# scripts attack pattern: inject_nonlinear_deviation
# status: success
def test_inject_nonlinear_deviation():
    startTime = time.time()
    attacked_df0 = test.inject_nonlinear_deviation('lat', 'lon', 'baroaltitude')
    endTime = time.time()
    print('The running time for [inject nonlinear deviation attack] is: %f s' % (endTime - startTime))
    for attacked_icao in test.get_attacked_targets():
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot(original_data[original_data.icao24 == attacked_icao[0]].lat,
                original_data[original_data.icao24 == attacked_icao[0]].lon,
                original_data[original_data.icao24 == attacked_icao[0]].baroaltitude,
                c='r', marker='*')
        ax.plot(attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lat,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].lon,
                attacked_df0[attacked_df0.icao24 == attacked_icao[0]].baroaltitude,
                c='b', marker='o')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')
        ax.set_zlabel('altitude')
        # plt.title('The tampering attack [inject nonlinear deviation] for %s' % attacked_icao)

    plt.show()


######## scripts execution ############
if __name__ == '__main__':
    test_inject_random_deviation()  # success
    # test_inject_constant_deviation()  # success
    # test_inject_increase_deviation()  # success, running for a long time
    # test_inject_changeable_deviation()  # success
    # test_inject_zoom_deviation()  # success
    # test_inject_nonlinear_deviation()  # success
