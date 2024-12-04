# Script is called Tensile-Part1-Processing.py
import pandas as pd  # reading and processing data

'''----- Beginning of Functions ---------------------------------------------'''
# Function to process and save data for a specific combination
def process_and_save_data(folder_location, combination, sequence_nums):
    combined_data = pd.DataFrame()  # Create empty DataFrame to store combined data
    # Pre Initialize Data Frame headers
    combined_data['Curve_Number'] = ''
    combined_data['Stress'] = ''
    combined_data['Strain'] = ''
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

        '''Calculating Stress [MPa] and Strain'''
        stress = df['Load [N]'].to_numpy() / 80.645     # Divide by 80.645 mm^2
        strain = df['Extension [mm]'].to_numpy() / 66.04  # Divide by 127 mm

        '''Saving Stress and Strain Data to combined DataFrame'''
        combined_data.loc[j, 'Curve_Number'] = curve_name
        combined_data.loc[j, 'Stress'] = f'{stress.tolist()}'
        combined_data.loc[j, 'Strain'] = f'{strain.tolist()}'
        combined_data.loc[j, 'Sequence'] = seq

    # Adding a description
    combined_data.loc[1, 'Comment'] = description

    # Save the combined data to a CSV file, in Processed-Tensile-Data
    output_file = f"Processed-Tensile-Data/{combination}_processed.csv"
    combined_data.to_csv(output_file, index=False)
    print(f"Saved results to: {output_file}")


'''----- End of Functions --------------------------------------------------'''

'''Mainline of Code - Beginning'''
# Defining sequence numbers for each color / temperature combination
# For Tensile Tests - Creating a Dictionary
file_groups = {
    # Red Color Combinations
    "Red_200": [5, 7, 9, 11], "Red_215": [27, 29, 36, 37],
    "Red_230": [44, 53, 54, 59],
    # Blue Color Combinations
    "Blue_200": [8, 12, 14, 19], "Blue_215": [22, 25, 32, 33],
    "Blue_230": [43, 50, 57, 58],
    # Green Color Combinations
    "Green_200": [10, 13, 15, 16], "Green_215": [23, 45, 52, 55],
    "Green_230": [34, 40, 46, 60],
    # Purple Color Combinations
    "Purple_200": [4, 6, 17, 18], "Purple_215": [24, 30, 35, 56],
    "Purple_230": [26, 39, 49, 51],
    # Black Color Combinations
    "Black_200": [1, 2, 3, 20], "Black_215": [21, 28, 41, 48],
    "Black_230": [31, 38, 42, 47],
}

# Folder name containing CSV files for tensile test results
data_folder = "Tensile-Data"

# Process each color/temperature combination within the file_groups dictionary
for combination_type, sequences in file_groups.items():
    # Calling on process_and_save_data function to process raw data
    process_and_save_data(data_folder, combination_type, sequences)
