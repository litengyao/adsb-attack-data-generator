"""
The script is used to generate the attack data set
author: Tengyao Li
date: 2019/04/30
"""

import logging

from attack_pattern.tampering_attack import tampering_attack
from attack_pattern.ghost_attack import ghost_attack
from attack_pattern.replay_attack import replay_attack
from attack_pattern.dos_attack import dos_attack

from data_io.read_adsb import reader

from util.parameter import DATA_ATTACK_SET_PATH, DATA_INPUT_PATH

if __name__ == "__main__":

    log = logging.getLogger('Attack Data Generator')

    dates = ["2019-12-23"]  # utilize the data on 2019-12-23

    for date in dates:
        year, month, day = date.split('-')
        log.info(("Generating Attack Data on %s" % date))

        io = reader(DATA_INPUT_PATH, year, month, day)
        original_df = io.get_continious_data(0, 0)  # configure the data source scale, this is the data of hour:0.

        attack_patterns = ['tampering', 'ghost', 'replay', 'dos', 'uncertainty']

        for attack_pattern in attack_patterns:
            if attack_pattern == 'tampering':

                attacker = tampering_attack(year, month, day)
                attacker.set_original_df(original_df.copy())
                attacker.set_attacked_targets(original_df.copy())

                attack_df0 = attacker.inject_random_deviation('lat', 'lon', 'baroaltitude')
                attack_df1 = attacker.inject_constant_deviation([2.5, 2.5, 2000], 'lat', 'lon', 'baroaltitude')
                attack_df2 = attacker.inject_increase_deviation([0.0005, 0.0005, 0.01], [0.0002, 0.0002, 0.000005],
                                                                'lat', 'lon',
                                                                'baroaltitude')
                attack_df3 = attacker.inject_changeable_deviation([0.25, 0.25, 200], 'lat', 'lon', 'baroaltitude')
                attack_df4 = attacker.inject_zoom_deviation([2.0, 3.0, 1.5], 'lat', 'lon', 'baroaltitude')
                attack_df5 = attacker.inject_nonlinear_deviation('lat', 'lon', 'baroaltitude')

                attack_df0.to_csv(DATA_ATTACK_SET_PATH + ("/attack_tampering_%s-random_deviation.csv" % date))
                attack_df1.to_csv(DATA_ATTACK_SET_PATH + ("/attack_tampering_%s-constant_deviation.csv" % date))
                attack_df2.to_csv(DATA_ATTACK_SET_PATH + ("/attack_tampering_%s-increase_deviation.csv" % date))
                attack_df3.to_csv(DATA_ATTACK_SET_PATH + ("/attack_tampering_%s-changeable_deviation.csv" % date))
                attack_df4.to_csv(DATA_ATTACK_SET_PATH + ("/attack_tampering_%s-zoom_deviation.csv" % date))
                attack_df5.to_csv(DATA_ATTACK_SET_PATH + ("/attack_tampering_%s-nonlinear_deviation.csv" % date))

                with open(DATA_ATTACK_SET_PATH + "/attack_tampering_targets.txt", 'w') as f:
                    targets = attacker.get_attacked_targets()
                    for target in targets:
                        f.write("%s, " % str(target))

            elif attack_pattern == 'ghost':

                attacker = ghost_attack(year, month, day)
                attacker.set_original_df(original_df.copy())
                attacker.set_attacked_targets(original_df.copy())

                ghost = 't12333'  # Issue: Please extend the single ghost to the ghost sets
                attack_df0, target_df0 = attacker.copy_ghost(ghost, 20.0, 30.0)
                attack_df1, target_df1 = attacker.create_ghost(ghost)
                attack_df2, target_df2 = attacker.random_ghost(ghost)

                attack_df0.to_csv(DATA_ATTACK_SET_PATH + ("/attack_ghost_%s-copy_ghost.csv" % date))
                attack_df1.to_csv(DATA_ATTACK_SET_PATH + ("/attack_ghost_%s-create_ghost.csv" % date))
                attack_df2.to_csv(DATA_ATTACK_SET_PATH + ("/attack_ghost_%s-random_ghost.csv" % date))

                with open(DATA_ATTACK_SET_PATH + "/attack_ghost_targets.txt", 'w') as f:
                    f.write(ghost)

            elif attack_pattern == 'replay':

                attacker = replay_attack(year, month, day)
                attacker.set_original_df(original_df.copy())
                attacker.set_attacked_targets(original_df.copy())

                attack_df0 = attacker.time_replay_attack(time_span=30)

                attack_df0.to_csv(DATA_ATTACK_SET_PATH + ("/attack_replay_%s-time_replay.csv" % date))

                with open(DATA_ATTACK_SET_PATH + "/attack_replay_targets.txt", 'w') as f:
                    targets = attacker.get_attacked_targets()
                    for target in targets:
                        f.write("%s, " % str(target))

            elif attack_pattern == 'dos':

                attacker = dos_attack(year, month, day)
                attacker.set_original_df(original_df.copy())
                attacker.set_attacked_targets(original_df.copy())

                attack_df0 = attacker.period_dos_attack(1511136550, 1511136910)
                attack_df1 = attacker.whole_dos_attack()
                attack_df2 = attacker.cycle_dos_attack(50, 30)

                attack_df0.to_csv(DATA_ATTACK_SET_PATH + ("/attack_dos_%s-period.csv" % date))
                attack_df1.to_csv(DATA_ATTACK_SET_PATH + ("/attack_dos_%s-whole.csv" % date))
                attack_df2.to_csv(DATA_ATTACK_SET_PATH + ("/attack_dos_%s-cycle.csv" % date))

                with open(DATA_ATTACK_SET_PATH + "/attack_dos_targets.txt", 'w') as f:
                    targets = attacker.get_attacked_targets()
                    for target in targets:
                        f.write("%s, " % str(target))

            else:
                # remaining for the uncertain attack patterns to add in the future
                pass
