# Script is called 3Point-Part4-AvgCurve_Comparison.py
import pandas as pd  # reading and processing data
import numpy as np
import matplotlib.pyplot as plt

'''----- Beginning of Functions ---------------------------------------------'''

def flex_stress_strain_from_csv(filelocation):
    # Function gathers INDIVIDUAL flexural curve stress and strain array

    # Reading csv file
    data_frame = pd.read_csv(filelocation)
    header_names = data_frame.columns.tolist()

    flex_stress = data_frame[f'{header_names[0]}'].to_numpy()
    flex_strain = data_frame[f'{header_names[1]}'].to_numpy()

    return flex_stress, flex_strain


def flex_curve_properties(array_flex_stress, array_flex_strain):
    # Function calculates INDIVIDUAL flexural curve properties
    # Properties: Flexural Modulus, and Flexural Yield Strength

    # Calculating the ultimate flexural strength
    ufs_idx = np.argmax(array_flex_stress)
    ufs = array_flex_stress[ufs_idx]
    linear_idx = int(ufs_idx / 5)

    # Calculating Young's Modulus
    linear_stress_segment = array_flex_stress[0:linear_idx]
    linear_strain_segment = array_flex_strain[0:linear_idx]

    # Getting linear line of best fit
    [slope, intercept] = np.polyfit(linear_strain_segment,
                                    linear_stress_segment, 1)
    flex_modulus = slope

    # Calculating the tensile yield strength
    # 0.2% offset for strain = 0.002 strain
    x_offset = 0.002
    offset_line = flex_modulus * (array_flex_strain - x_offset)

    stress_difference = array_flex_stress - offset_line

    # np.where outputs a tuple, so we have to pass two index values
    intersect_index = np.where(stress_difference <= 0)[0][0]

    flex_yield_strength = array_flex_stress[intersect_index]

    return flex_modulus, flex_yield_strength


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
avg_curve_props['Flexural_Modulus'] = ''
avg_curve_props['Flex_Yield_Strength'] = ''

counter = 1

''' Main Code '''
for temp_group, category in temp_groups.items():
    # Folder name containing CSV files for flexural test results
    data_folder = "3Point-Average-Graphs"

    # Making Descriptions and Save Paths
    group_temperature = (f"{temp_group}".replace('Temp_','')
                         .replace('C', '°C'))
    graph_description = f"3 Point Bending Comparison of Colors at {group_temperature}"
    png_save_path = f"3Point-Results/Color_Comparison_{temp_group}.png"

    # Initializing a figure
    plt.figure(figsize=(10, 6))

    # Note: Graphing Black, Blue, Green, Purple and then Red

    for i, combination in enumerate(category):
        # Curve Description
        color_temp = f"{combination}"
        file_path = f"{data_folder}/Average_{color_temp}.csv"
        curve_description = (color_temp.replace('_',' ').
                             replace('C', '°C'))

        [current_flexstress, current_flexstrain] = flex_stress_strain_from_csv(file_path)

        [current_flex_modulus, current_flex_yieldstrength] \
            = flex_curve_properties(current_flexstress, current_flexstrain)

        avg_curve_props.loc[counter, 'Description'] = combination
        avg_curve_props.loc[counter, 'Flexural_Modulus'] = current_flex_modulus
        avg_curve_props.loc[counter, 'Flex_Yield_Strength'] \
            = current_flex_yieldstrength

        counter = counter + 1

        plt.plot(current_flexstrain, current_flexstress,
                 label=curve_description, color=color_order[i])

    # Labeling
    plt.title(graph_description)
    plt.xlabel("Flexural Strain")
    plt.ylabel("Flexural Stress [MPa]")
    plt.legend()
    plt.grid(True)

    # Saving plot then showing it
    plt.savefig(png_save_path, dpi=600)
    print(f"Saved plot to: {png_save_path}")

    plt.show()

# Saving Average Curve Properties to CSV file
csv_path = f"3Point-Results/Average_Curve_Flex_Properties.csv"
avg_curve_props.to_csv(csv_path, index=False)

print(f"Saved csv to: {csv_path}")