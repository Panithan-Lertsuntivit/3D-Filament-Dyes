# Script is called Tensile-Part5-AverageCurve_Comparison.py
import pandas as pd  # reading and processing data
import numpy as np
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


def tensile_curve_properties(array_stress, array_strain):
    # Function calculates INDIVIDUAL tensile curve properties
    # Properties: Ultimate Tensile Strength, Young's Modulus, and Yield Strength

    # Calculating the ultimate tensile strength
    uts_idx = np.argmax(array_stress)
    uts = array_stress[uts_idx]
    linear_idx = int(uts_idx / 5)

    # Calculating Young's Modulus
    linear_stress_segment = array_stress[0:linear_idx]
    linear_strain_segment = array_strain[0:linear_idx]

    # Getting linear line of best fit
    [slope, intercept] = np.polyfit(linear_strain_segment,
                                    linear_stress_segment, 1)
    young_modulus = slope

    # Calculating the tensile yield strength
    # 0.2% offset for strain = 0.002 strain
    x_offset = 0.002
    offset_line = young_modulus * (array_strain - x_offset)

    stress_difference = array_stress - offset_line

    # np.where outputs a tuple, so we have to pass two index values
    intersect_index = np.where(stress_difference <= 0)[0][0]

    yield_strength = array_stress[intersect_index]

    return uts, young_modulus, yield_strength


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

tester = {
    # Temperature at 230C
    "Temp_230C": ['Black_230C', 'Blue_230C', 'Green_230C',
                  'Purple_230C', 'Red_230C'],
}

color_order = ['black', 'dodgerblue', 'forestgreen', 'darkviolet', 'crimson']

# Predefine Pandas Dataframe
avg_curve_props = pd.DataFrame()
avg_curve_props['Description'] = ''
avg_curve_props['UTS'] = ''
avg_curve_props['Young_Modulus'] = ''
avg_curve_props['Yield_Strength'] = ''

counter = 1

''' Main Code '''
for temp_group, category in temp_groups.items():
    # Folder name containing CSV files for tensile test results
    data_folder = "Tensile-Average-Graphs"

    # Making Descriptions and Save Paths
    group_temperature = (f"{temp_group}".replace('Temp_','')
                         .replace('C', '°C'))
    graph_description = f"Tensile Comparison of Colors at {group_temperature}"
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

        [current_uts, current_youngmodulus, current_yieldstrength] \
            = tensile_curve_properties(current_stress, current_strain)

        avg_curve_props.loc[counter, 'Description'] = combination
        avg_curve_props.loc[counter, 'UTS'] = current_uts
        avg_curve_props.loc[counter, 'Young_Modulus'] = current_youngmodulus
        avg_curve_props.loc[counter, 'Yield_Strength'] = current_yieldstrength

        counter = counter + 1

        plt.plot(current_strain, current_stress,
                 label=curve_description, color=color_order[i])

    # Labeling
    plt.title(graph_description)
    plt.xlabel("Strain")
    plt.ylabel("Stress [MPa]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Saving plot then showing it
    plt.savefig(png_save_path, dpi=600)
    print(f"Saved plot to: {png_save_path}")

    plt.show()

# Saving Average Curve Properties to CSV file
csv_path = f"Tensile-Results/Average_Curve_Properties.csv"
avg_curve_props.to_csv(csv_path, index=False)

print(f"Saved csv to: {csv_path}")




