# Script is called Tensile-Part5-AverageCurve_Comparison.py
import pandas as pd  # reading and processing data
import numpy as np
import ast
import matplotlib.pyplot as plt

'''----- Beginning of Functions ---------------------------------------------'''

def stress_strain_from_csv(filelocation):
    # Function gathers INDIVIDUAL tensile curve stress and strain array

    # Reading csv file
    data_frame = pd.read_csv(filelocation)
    header_names = data_frame.columns.tolist()

    stress = data_frame[f'{header_names[0]}'].to_numpy()
    strain = data_frame[f'{header_names[1]}'].to_numpy()

    return stress, strain


'''----- End of Functions --------------------------------------------------'''

'''Mainline of Code - Beginning'''
# For Tensile Average Tests - Creating a Dictionary based on Temperature
temp_groups = {
    # Temperature Combinations
    # Temperature at 200C
    "Temp_200C": ['Black_200C', 'Blue_200C', 'Green_200C',
                  'Purple_200C', 'Red_200C'],
    # Temperature at 215C
    "Temp_215C": ['Black_215C', 'Blue_215C', 'Green_215C',
                  'Purple_215C', 'Red_215C'],
    # Temperature at 230C
    "Temp_230C": ['Black_230C', 'Blue_230C', 'Green_230C',
                  'Purple_230C', 'Red_230C'],
}

# tester = {
#     # Temperature at 200C
#     "Temp_200C": ['Black_200C', 'Blue_200C', 'Green_200C',
#                   'Purple_200C', 'Red_200C'],
# }

color_order = ['black', 'dodgerblue', 'forestgreen', 'darkviolet', 'crimson']

''' Main Code '''
for temp_group, category in temp_groups.items():
    # Folder name containing CSV files for tensile test results
    data_folder = "Tensile-Average-Graphs"

    # Making Descriptions and Save Paths
    group_temperature = (f"{temp_group}".replace('Temp_','')
                         .replace('C', '°C'))
    graph_description = f"Comparison of Colors at {group_temperature}"
    png_save_path = f"Tensile-Results/Color_Comparison_{temp_group}.png"

    # Initializing a figure
    plt.figure(figsize=(10, 6))

    # Note: Graphing Black, Blue, Green, Purple and then Red

    for i, combination in enumerate(category):
        # Curve Description
        color_temp = f"{combination}"
        file_path = f"{data_folder}/Average_{color_temp}.csv"
        curve_description = (color_temp.replace('_',' ').
                             replace('C', '°C'))

        [current_stress, current_strain] = stress_strain_from_csv(file_path)

        plt.plot(current_strain, current_stress,
                 label=curve_description, color=color_order[i])

    # Labeling
    plt.title(graph_description)
    plt.xlabel("Strain")
    plt.ylabel("Stress [MPa]")
    plt.legend()
    plt.grid(True)

    # Saving plot then showing it
    plt.savefig(png_save_path, dpi=600)
    print(f"Saved plot to: {png_save_path}")

    plt.show()


