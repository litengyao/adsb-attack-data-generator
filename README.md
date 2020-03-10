## adsb-attack-data-generator
Generate ADS-B Attack Data for Classical Attack Patterns

> The project is only for researches, please do not utilize the codes to implement 
> attack behaviors in real air traffic environments.

The scripts are designed to reproduce the data disruptions for ADS-B data attack, which
are the simulation codes for the paper "Threat Model and Construction Strategy on ADS-B Attack Data".

### 1. Running Requirements
- Anaconda (Python 3.x edition)
- opensky_api (To obtain this package, please refer to https://opensky-network.org/apidoc/python.html)

### 2. Module Functions

- scripts The execution scripts
  - main.py  :The entrance code for the whole experiment, which is utilized to implement automatic generation procedure.
  - t_tampering_attack :The test script for data manipulation attack
  - t_ghost_attack :The test script for ghost injection attack
  - t_replay_attack :The test script for data replay attack
  _ t_dos_attack :The test script for data block attack (DoS)
- attack :The core module for attack patterns
  - attack :The basic class for attack patterns
  - dos_attack :DoS attack disruption on ADS-B data
  - ghost_attack :Ghost injection attack disruption on ADS-B data
  - replay_attack :Replay attack disruption on ADS-B data
  - tampering_attack :Data manipulation attack disruption on ADS-B data
- attack_choice :The strategy to choose the attacked flight targets
- basic_processor :Data processing and visualization
- data_collector :Collect data from OpenSky-Network
- data_io :Read/Write ADS-B data from disks

### 3. Develop

If you want to develop the code, please inherit the class: attack to extend new attack patterns.