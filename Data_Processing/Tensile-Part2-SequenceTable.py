# Script is called Tensile-Part2-SequenceTable.py
import pandas as pd  # reading and processing data
import numpy as np
import ast
import matplotlib.pyplot as plt

'''----- Beginning of Functions ---------------------------------------------'''

def stress_strain_seq_from_csv(filelocation):
    # Initialize arrays
    array_stresses = []
    array_strains = []
    array_sequence_nums = []

    # Reading csv file
    data_frame = pd.read_csv(filelocation)
    header_names = data_frame.columns.tolist()
    num_rows = len(data_frame.index)

    for j in range(num_rows):
        # Extracting stress, strain and sequence number and saving to arrays
        stress = data_frame.loc[j, f'{header_names[1]}']
        strain = data_frame.loc[j, f'{header_names[2]}']
        sequence_num = data_frame.loc[j, f'{header_names[3]}']

        # Convert to string to list (ast.literal_eval) then convert to np array
        stress = np.array(ast.literal_eval(stress))
        strain = np.array(ast.literal_eval(strain))

        array_stresses.append(stress)
        array_strains.append(strain)
        array_sequence_nums.append(sequence_num)

    return array_stresses, array_strains, array_sequence_nums


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
    yield_strain = array_strain[intersect_index]

    # ''' Graphing '''
    # # # Find yield strength
    # # yield_strength, yield_strain, offset_line = find_yield_strength(strain,
    # #                                                                 stress)
    # # Plot the results
    # plt.figure(figsize=(8, 6))
    # plt.plot(array_strain, array_stress, label="Stress-Strain Curve")
    # plt.plot(array_strain, offset_line, "--", label="0.2% Offset Line")
    # plt.scatter(yield_strain, yield_strength, color="red",
    #             label=f"Yield Strength: {yield_strength:.2f} MPa")
    # plt.axhline(y=yield_strength, color="red", linestyle="--", alpha=0.7)
    # plt.axvline(x=yield_strain, color="red", linestyle="--", alpha=0.7)
    # plt.xlabel("Strain")
    # plt.ylabel("Stress (MPa)")
    # plt.title("Yield Strength Determination")
    # plt.legend()
    # plt.grid()
    # plt.show()

    return uts, young_modulus, yield_strength


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
    # "Red_200_processed.csv",
    # "Red_215_processed.csv",
    # "Red_230_processed.csv",
    "Black_200_processed.csv",
]

# Initializing DataFrame for Sequence UTS, Young's Modulus, Yield Strength
sequence_table = pd.DataFrame()
sequence_table['Sequence_Number'] = ''
sequence_table['Color'] = ''
sequence_table['Temperature'] = ''
sequence_table['UTS'] = ''
sequence_table['Young_Modulus'] = ''
sequence_table['Yield_Strength'] = ''

seq_counter = 1

# Category Average and Standard Deviation for UTS, Young's Modulus, Toughness
category_table = pd.DataFrame()
category_table['Category'] = ''
category_table['AVG_UTS'] = ''
category_table['STD_UTS'] = ''
category_table['AVG_YoungModulus'] = ''
category_table['STD_YoungModulus'] = ''
category_table['AVG_Yield_Strength'] = ''
category_table['STD_Yield_Strength'] = ''

category_counter = 1

''' Beginning of for loop iteration '''
for file_name in processed_file_names:
    folder_name = f"Tensile-Processed-Data"

    # Creating the file location
    file_location = f"{folder_name}/{file_name}"

    description = file_name.replace('_processed.csv', '')
    [color, temperature] = description.split('_')
    category_table.loc[category_counter, 'Category'] = description

    ''' Getting Stress / Strain and Calculating Average Curve - - - - - - - '''
    # Function to read stress/strain from csv file
    [stress_curves, strain_curves, sequence_nums] \
        = stress_strain_seq_from_csv(file_location)

    # Initialize Arrays
    uts_array = []
    young_modulus_array = []
    yield_strength_array = []

    j = 0

    for seq in sequence_nums:
        # Function to get UTS, E (Young's Modulus), and Toughness
        [seq_uts, seq_young_modulus, seq_yield_strength] \
            = tensile_curve_properties(stress_curves[j], strain_curves[j])

        '''Information to DataFrame'''
        sequence_table.loc[seq_counter, 'Sequence_Number'] = seq
        sequence_table.loc[seq_counter, 'UTS'] = seq_uts
        sequence_table.loc[seq_counter, 'Young_Modulus'] = seq_young_modulus
        sequence_table.loc[seq_counter, 'Yield_Strength'] = seq_yield_strength
        sequence_table.loc[seq_counter, 'Color'] = color
        sequence_table.loc[seq_counter, 'Temperature'] = temperature

        '''Saving values to array - to calculate std and averages'''
        uts_array.append(seq_uts)
        young_modulus_array.append(seq_young_modulus)
        yield_strength_array.append(seq_yield_strength)

        j = j + 1
        seq_counter = seq_counter + 1

    ''' Calculating Averages and STD, then save to DataFrame '''
    category_table.loc[category_counter, 'AVG_UTS'] \
        = np.average(uts_array)
    category_table.loc[category_counter, 'AVG_YoungModulus'] \
        = np.average(young_modulus_array)
    category_table.loc[category_counter, 'AVG_Yield_Strength'] \
        = np.average(yield_strength_array)

    category_table.loc[category_counter, 'STD_UTS'] \
        = np.std(uts_array, ddof=1)
    category_table.loc[category_counter, 'STD_YoungModulus'] \
        = np.std(young_modulus_array, ddof=1)
    category_table.loc[category_counter, 'STD_Yield_Strength'] \
        = np.std(yield_strength_array, ddof=1)

    category_counter = category_counter + 1

''' End of for loop iteration '''

# Save the DataFrames to a CSV file, in Tensile-Results
sequence_output_file = f"Tensile-Results/Table_Sequences.csv"
category_output_file = f"Tensile-Results/Table_Categories.csv"

sorted_sequence_table = sequence_table.sort_values(by=['Sequence_Number'],
                                                   ascending=True)

sorted_sequence_table.to_csv(sequence_output_file, index=False)
category_table.to_csv(category_output_file, index=False)

print(f"Saved sequence table to: {sequence_output_file} \n")
print(f"Saved category table to: {category_output_file} \n")

