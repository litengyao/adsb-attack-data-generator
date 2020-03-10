"""
@function: scripts the ghost attack
@author: Tengyao Li
@date: 2018/09/30
@status: developing
@code-type: testing script
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from attack_pattern import ghost_attack

# scripts the parent class: attack_pattern [3 functions]
# status: success
test = ghost_attack.ghost_attack(2019, 12, 23, 0, 0)
# print(scripts.get_attacked_targets())
# print('The percent of attacked flights is:\t %f' % scripts.get_attacked_percent())
original_data = test.get_original_df()


# scripts attack pattern: copy ghost attack
# status: testing
def test_copy_ghost():
    startTime = time.time()
    attacked_df, cur_df = test.copy_ghost('t12333', 20.0, 30.0)
    endTime = time.time()
    print('The running time for [copy ghost attack] is: %f s' % (endTime - startTime))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot(cur_df.lat, cur_df.lon, cur_df.baroaltitude, c='b', marker='o')
    ax.set_xlabel('latitude')
    ax.set_ylabel('longitude')
    ax.set_zlabel('altitude')
    # plt.title('The ghost attack [copy ghost] for %s' % cur_df.icao24[0])
    plt.show()


# scripts attack pattern: create ghost attack
# status: testing
def test_create_ghost():
    startTime = time.time()
    attacked_df, cur_df = test.create_ghost('t12333')
    endTime = time.time()
    print('The running time for [create ghost attack] is: %f s' % (endTime - startTime))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot(cur_df.lat, cur_df.lon, cur_df.baroaltitude, c='b', marker='o')
    ax.set_xlabel('latitude')
    ax.set_ylabel('longitude')
    ax.set_zlabel('altitude')
    # plt.title('The ghost attack [create ghost]')
    plt.show()


# scripts attack pattern: random ghost attack
# status: testing
def test_random_ghost():
    startTime = time.time()
    attacked_df, cur_df = test.random_ghost('t12333')
    endTime = time.time()
    print('The running time for [random ghost attack] is: %f s' % (endTime - startTime))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot(cur_df.lat, cur_df.lon, cur_df.baroaltitude, c='b', marker='o')
    ax.set_xlabel('latitude')
    ax.set_ylabel('longitude')
    ax.set_zlabel('altitude')
    # plt.title('The ghost attack [random ghost] for %s' % cur_df.iloc[0].loc['icao24'])
    plt.show()

######## scripts execution ############
# test_copy_ghost() # success
# test_create_ghost() # success
test_random_ghost() # success