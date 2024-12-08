# Script is called 3Point-Part2-SequenceTable.py
import pandas as pd  # reading and processing data
import numpy as np
import ast

'''----- Beginning of Functions ---------------------------------------------'''



'''----- End of Functions --------------------------------------------------'''


'''Mainline of Code - Beginning'''
# Defining file names for each color / temperature combination
# For Processed Tensile Tests - Creating a List
processed_file_names = [
    # Red Color Combinations
    "Red_200_processed.csv", "Red_215_processed.csv", "Red_230_processed.csv",
    # Blue Color Combinations
    "Blue_200_processed.csv", "Blue_215_processed.csv",
    "Blue_230_processed.csv",
    # Green Color Combinations
    "Green_200_processed.csv", "Green_215_processed.csv",
    "Green_230_processed.csv",
    # Purple Color Combinations
    "Purple_200_processed.csv", "Purple_215_processed.csv",
    "Purple_230_processed.csv",
    # Black Color Combinations
    "Black_200_processed.csv", "Black_215_processed.csv",
    "Black_230_processed.csv",
]

temp_file_names = [
    # Red Color Combinations
    "Red_200_processed.csv",
    "Red_215_processed.csv",
    "Red_230_processed.csv",
]

# Initializing DataFrame for Sequence UTS, Young's Modulus, Toughness
sequence_table_3point = pd.DataFrame()
sequence_table_3point['Sequence_Number'] = ''
sequence_table_3point['UTS'] = ''
sequence_table_3point['Young_Modulus'] = ''
sequence_table_3point['Toughness'] = ''
sequence_table_3point['Color/Temperature'] = ''