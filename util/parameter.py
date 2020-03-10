################################################
# The constant variables for the whole project #
################################################
import os

DATA_SOURCE_PATH = "https://opensky-network.org/datasets/states/"

DATA_BASIC_PATH = os.path.abspath('..') + "/data"
DATA_ONLINE_PATH = DATA_BASIC_PATH + "/online"  # the data obtained online for real time
DATA_INPUT_PATH = DATA_BASIC_PATH + "/original"  # the csv files that contain the original ADS-B decoded data
DATA_COLLECTED_PATH = DATA_BASIC_PATH + "/collected"  # the tar.gz files downloaded from opensky-network.org
DATA_SELECTED_PATH = DATA_BASIC_PATH + "/selected"  # the preprocessed ADS-B data without missing values
DATA_ATTACK_SET_PATH = DATA_BASIC_PATH + "/attack"  # the attack data constructed with models
DATA_OUTPUT_PATH = DATA_BASIC_PATH + "/output"  # the detection results

DATA_VISUALIZATION_PATH = DATA_BASIC_PATH + "/plot"  # the intermediate figures
DATA_AWARENESS_SCENE_PATH = DATA_BASIC_PATH + "/awareness"  # the situation awareness visualizations
