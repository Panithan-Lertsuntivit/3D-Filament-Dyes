# Script is called 3Point-Part2-SequenceTable.py
import pandas as pd  # reading and processing data
import numpy as np
import ast

'''----- Beginning of Functions ---------------------------------------------'''

def flex_stress_strain_seq_from_csv(filelocation):
    # Initialize arrays
    array_flex_stresses = []
    array_flex_strains = []
    array_sequence_nums = []

    # Reading csv file
    data_frame = pd.read_csv(filelocation)
    header_names = data_frame.columns.tolist()
    num_rows = len(data_frame.index)

    for k in range(num_rows):
        # Extracting stress, strain and sequence number and saving to arrays
        stress = data_frame.loc[k, f'{header_names[1]}']
        strain = data_frame.loc[k, f'{header_names[2]}']
        sequence_num = data_frame.loc[k, f'{header_names[3]}']

        # Convert to string to list (ast.literal_eval) then convert to np array
        stress = np.array(ast.literal_eval(stress))
        strain = np.array(ast.literal_eval(strain))

        array_flex_stresses.append(stress)
        array_flex_strains.append(strain)
        array_sequence_nums.append(sequence_num)

    return array_flex_stresses, array_flex_strains, array_sequence_nums

def flexural_curve_properties(array_flex_stress, array_flex_strain):
    # Function calculates INDIVIDUAL tensile curve properties
    # Properties: Flexural Modulus, and Flexural Yield Strength

    # Calculating the ultimate flexural strength
    uts_idx = np.argmax(array_flex_stress)
    ultimate_flex_strength = array_flex_stress[uts_idx]
    linear_idx = int(uts_idx / 5)

    # Calculating Young's Modulus
    linear_stress_segment = array_flex_stress[0:linear_idx]
    linear_strain_segment = array_flex_strain[0:linear_idx]

    # Getting linear line of best fit
    [slope, intercept] = np.polyfit(linear_strain_segment,
                                    linear_stress_segment, 1)
    flexural_modulus = slope

    # Calculating the tensile yield strength
    # 0.2% offset for strain = 0.002 strain
    x_offset = 0.002
    offset_line = flexural_modulus * (array_flex_strain - x_offset)

    flex_stress_difference = array_flex_stress - offset_line

    # np.where outputs a tuple, so we have to pass two index values
    intersect_index = np.where(flex_stress_difference <= 0)[0][0]

    flexural_yield_strength = array_flex_stress[intersect_index]

    return flexural_modulus, flexural_yield_strength

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

# Initializing DataFrame for Sequence, Flexural Modulus, Flex_Yield Strength
sequence_table = pd.DataFrame()
sequence_table['Sequence_Number'] = ''
sequence_table['Color'] = ''
sequence_table['Temperature'] = ''
sequence_table['Flex_Modulus'] = ''
sequence_table['Flex_Yield_Strength'] = ''

seq_counter = 1

# Category AVG and STD for Flexural Modulus, Flex Yield Strength
category_table = pd.DataFrame()
category_table['Category'] = ''
category_table['AVG_FlexModulus'] = ''
category_table['STD_FlexModulus'] = ''
category_table['AVG_FlexYield_Strength'] = ''
category_table['STD_FlexYield_Strength'] = ''

category_counter = 1

''' Beginning of for loop iteration '''
for file_name in processed_file_names:
    folder_name = f"3Point-Processed-Data"

    # Creating the file location
    file_location = f"{folder_name}/{file_name}"

    description = file_name.replace('_processed.csv', '')
    [color, temperature] = description.split('_')
    category_table.loc[category_counter, 'Category'] = description

    ''' Getting Stress / Strain and Calculating Average Curve - - - - - - - '''
    # Function to read stress/strain from csv file
    [flexstress_curves, flexstrain_curves, sequence_nums] \
        = flex_stress_strain_seq_from_csv(file_location)

    # Initialize Arrays
    flex_modulus_array = []
    flex_yield_strength_array = []

    j = 0

    for seq in sequence_nums:
        # Function to get UTS, E (Young's Modulus), and Toughness
        [seq_flex_modulus, seq_flex_yield_strength] \
            = flexural_curve_properties(flexstress_curves[j], flexstrain_curves[j])

        '''Information to DataFrame'''
        sequence_table.loc[seq_counter, 'Sequence_Number'] = seq
        sequence_table.loc[seq_counter, 'Flex_Modulus'] = seq_flex_modulus
        sequence_table.loc[seq_counter, 'Flex_Yield_Strength'] = seq_flex_yield_strength
        sequence_table.loc[seq_counter, 'Color'] = color
        sequence_table.loc[seq_counter, 'Temperature'] = temperature

        '''Saving values to array - to calculate std and averages'''
        flex_modulus_array.append(seq_flex_modulus)
        flex_yield_strength_array.append(seq_flex_yield_strength)

        j = j + 1
        seq_counter = seq_counter + 1

    ''' Calculating Averages and STD, then save to DataFrame '''
    category_table.loc[category_counter, 'AVG_FlexModulus'] \
        = np.average(flex_modulus_array)
    category_table.loc[category_counter, 'AVG_FlexYield_Strength'] \
        = np.average(flex_yield_strength_array)

    category_table.loc[category_counter, 'STD_FlexModulus'] \
        = np.std(flex_modulus_array, ddof=1)
    category_table.loc[category_counter, 'STD_FlexYield_Strength'] \
        = np.std(flex_yield_strength_array, ddof=1)

    category_counter = category_counter + 1

''' End of for loop iteration '''

# Save the DataFrames to a CSV file, in Tensile-Results
sequence_output_file = f"3Point-Results/Table_Flex_Sequences.csv"
category_output_file = f"3Point-Results/Table_Flex_Categories.csv"

sorted_sequence_table = sequence_table.sort_values(by=['Sequence_Number'],
                                                   ascending=True)

sorted_sequence_table.to_csv(sequence_output_file, index=False)
category_table.to_csv(category_output_file, index=False)

print(f"Saved sequence table to: {sequence_output_file} \n")
print(f"Saved category table to: {category_output_file} \n")