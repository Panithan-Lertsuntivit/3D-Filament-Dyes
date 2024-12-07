# Script is called Tensile-Part1-Processing.py
import pandas as pd  # reading and processing data
import numpy as np


'''----- Beginning of Functions ---------------------------------------------'''
# Function to process and save data for a specific combination
def process_and_save_data(folder_location, combination, sequence_nums):
    combined_data = pd.DataFrame()  # Create empty DataFrame to store combined data
    # Pre Initialize Data Frame headers
    combined_data['Curve_Number'] = ''
    combined_data['Flex_Stress'] = ''
    combined_data['Flex_Strain'] = ''
    combined_data['Sequence'] = ''
    combined_data['Comment'] = ''

    # Creating a Description
    color_temp = f"{combination.replace('-', ' ')}"
    sequence_list = str(sequence_nums)
    # Getting rid of the brackets in sequence_list
    sequence_numbers = sequence_list.replace('[', '').replace(']', '')

    description = f"{color_temp}, Seq: {sequence_numbers}"

    for i, seq in enumerate(sequence_nums):
        j = i + 1       # Shifting it up by 1 so j will start at 1 and not 0

        file_path = f"{folder_location}/Sequence_{seq}.csv"
        curve_name = f"Curve_{j}"

        '''Reading CSV and Formatting'''
        # Read the CSV file, actual data starts at row 6 (so skip 5 rows)
        df = pd.read_csv(file_path, skiprows=5)
        # First row after the headers are just units, dropping that row
        df.drop([0], inplace=True)

        # Rename Columns to have Units
        df.columns = ['Time [s]', 'Extension [mm]', 'Load [N]']
        # Keeping only the Extension and Load Columns
        df = df[['Extension [mm]', 'Load [N]']]

        # Converting to Numeric Data Types, if it isn't already numeric
        df['Extension [mm]'] = pd.to_numeric(df['Extension [mm]'],
                                             errors='coerce')
        df['Load [N]'] = pd.to_numeric(df['Load [N]'], errors='coerce')

        ''' Removing the initial noise - using find_increasing_index() '''
        # find_increasing_index() takes only np arrays
        unfiltered_load = df['Load [N]'].to_numpy()
        unfiltered_extension = df['Extension [mm]'].to_numpy()

        increasing_idx = find_increasing_index(unfiltered_load)

        filtered_load_N = unfiltered_load[increasing_idx:]
        filtered_deflection_mm = (unfiltered_extension[increasing_idx:] -
                               unfiltered_extension[increasing_idx])

        '''Calculating Flexural Stress [MPa] and Strain'''
        # 3 Point Bending Dimensions
        length_mm = 101.6       # Support Span Length
        width_mm = 19.05        # Width
        thickness_mm = 6.35     # Thickness or height

        flex_stress_kPa = ((3 * filtered_load_N * length_mm) /
                       (2 * width_mm * thickness_mm))
        flex_stress_MPa = flex_stress_kPa * (pow(10, -3))
        flex_strain = ((6 * thickness_mm * filtered_deflection_mm) /
                       pow(length_mm, 2))

        '''Saving Stress and Strain Data to combined DataFrame'''
        combined_data.loc[j, 'Curve_Number'] = curve_name
        combined_data.loc[j, 'Flex_Stress'] = f'{flex_stress_MPa.tolist()}'
        combined_data.loc[j, 'Flex_Strain'] = f'{flex_strain.tolist()}'
        combined_data.loc[j, 'Sequence'] = seq

    # Adding a description
    combined_data.loc[1, 'Comment'] = description

    # Save the combined data to a CSV file, in Processed-Tensile-Data
    output_file = f"3PointBending-Processed-Data/{combination}_processed.csv"
    combined_data.to_csv(output_file, index=False)
    print(f"Saved results to: {output_file}")


def find_increasing_index(y_values):
    # Function finds the first index of an increasing pattern (above the
    # set tolerance)
    tolerance = 0.50
    less_than_tolerance = np.where(y_values < tolerance)

    # Getting the last index of array
    # Note: np.where outputs a tuple, so we want the first tuple item (use [0])
    first_increasing_idx = less_than_tolerance[0][-1]

    return first_increasing_idx
    




'''----- End of Functions --------------------------------------------------'''

'''Mainline of Code - Beginning'''
# Defining sequence numbers for each color / temperature combination
# For 3 Point Bend Tests - Creating a Dictionary
file_groups = {
    # Red Color Combinations
    "Red_200": [1, 5, 16, 56], "Red_215": [3, 25, 30, 37],
    "Red_230": [9, 46, 53, 58],
    # Green Color Combinations
    "Green_200": [6, 13, 28, 34], "Green_215": [26, 40, 41, 48],
    "Green_230": [15, 45, 49, 54],
    # Blue Color Combinations
    "Blue_200": [7, 31, 39, 47], "Blue_215": [14, 20, 29, 55],
    "Blue_230": [2, 4, 33, 44],
    # Purple Color Combinations
    "Purple_200": [12, 22, 23, 59], "Purple_215": [24, 32, 51, 60],
    "Purple_230": [11, 19, 36, 57],
    # Black Color Combinations
    "Black_200": [17, 21, 43, 50], "Black_215": [18, 35, 38, 42],
    "Black_230": [8, 10, 27, 52],
}

tester_group = {
    # Red Color Combinations
    "Red_200": [1, 5, 16, 56],
    # "Red_215": [3, 25, 30, 37],
    # "Red_230": [9, 46, 53, 58],
}

# Folder name containing CSV files for tensile test results
data_folder = "3PointBending-Data"

# Process each color/temperature combination within the file_groups dictionary
for combination_type, sequences in file_groups.items():
    # Calling on process_and_save_data function to process raw data
    process_and_save_data(data_folder, combination_type, sequences)