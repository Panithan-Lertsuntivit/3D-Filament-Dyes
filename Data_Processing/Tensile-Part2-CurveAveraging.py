# Script is called Tensile-Part2-CurveAveraging.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

'''----- Beginning of Functions --------------------------------------------'''

def stress_strain_from_csv(filelocation):

    # Initialize arrays
    array_stresses = []
    array_strains = []

    # Reading csv file
    data_frame = pd.read_csv(filelocation)
    header_names = data_frame.columns.tolist()
    num_rows = len(data_frame.index)

    for j in range(num_rows):
        # Extracting stress/strain information and then saving them to arrays
        stress = data_frame.loc[j, f'{header_names[1]}']
        strain = data_frame.loc[j, f'{header_names[2]}']

        # Convert to string to list (ast.literal_eval) then convert to np array
        stress = np.array(ast.literal_eval(stress))
        strain = np.array(ast.literal_eval(strain))

        array_stresses.append(stress)
        array_strains.append(strain)

    return array_stresses, array_strains


def avg_uts_stressdrop_with_num_elements(array_stresses, array_strains):

    ultimate_tensile_stresses = []
    stress_drops_after_UTS = []
    elements_rise = 0
    elements_fall = 0

    for j, stresses in enumerate(array_stresses):
        # Finding the UTS and its index
        ultimate_tensile_stresses.append(max(stresses))
        uts_idx = np.argmax(stresses)

        # Splitting the arrays at the UTS (UTS value goes to rising trend)
        rising_stress = stresses[0:uts_idx + 1]
        falling_stress = stresses[uts_idx + 2:]

        # Keeping track of elements
        if len(rising_stress) > elements_rise:
            elements_rise = len(rising_stress)

        if len(falling_stress) > elements_fall:
            elements_fall = len(falling_stress)

        current_stress_drop = falling_stress[-1] - rising_stress[-1]
        stress_drops_after_UTS.append(current_stress_drop)

    # Calculating Averages - Used in interpolation
    average_uts = np.mean(ultimate_tensile_stresses)
    average_stress_drop = np.mean(stress_drops_after_UTS)

    return average_uts, average_stress_drop, elements_rise, elements_fall


def split_at_uts(stress_values, strain_values):

    # Finding the UTS index
    uts_idx = np.argmax(stress_values)

    # Splitting the arrays at the UTS (UTS value goes to rising trend)
    rising_stress = stress_values[0:uts_idx+1]
    falling_stress = stress_values[uts_idx+2:]

    rising_strain = strain_values[0:uts_idx+1]
    falling_strain = strain_values[uts_idx+2:]

    return (rising_stress, falling_stress, rising_strain,
            falling_strain)


def interpolate_avg_curve(tg_stress_avg, num_elements, array_stresses, array_strains):

    avg_stress_axis = np.linspace(0, tg_stress_avg, num_elements)
    # TG (Target)

    interpolated_strain_axes = []
    # INTERP (interpolate)
    for k in range(len(array_stresses)):
        strain_interp_axis = np.interp(avg_stress_axis,
                                       array_stresses[k], array_strains[k])
        interpolated_strain_axes.append(strain_interp_axis)

    avg_strain_axis = np.mean(interpolated_strain_axes, axis=0)

    return avg_stress_axis, avg_strain_axis


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

# temp_file_names = [# Red Color Combinations
#     "Red_200_processed.csv",
#     # "Red_215_processed.csv",
#     # "Red_230_processed.csv",
# ]

# Main For loop
for file_name in processed_file_names:
    folder_name = f"Processed-Tensile-Data"

    # Creating the file location
    file_location = f"{folder_name}/{file_name}"

    ''' Getting Stress / Strain and Calculating Average Curve - - - - - - - '''
    # Function to read stress/strain from csv file
    [stress_curves, strain_curves] = stress_strain_from_csv(file_location)

    # Function to get avg UTS and stress drop, along with num elements
    [avg_uts, avg_stressdrop, num_element_rise, num_element_fall] \
        = avg_uts_stressdrop_with_num_elements(stress_curves, strain_curves)

    # Splitting stress/strain curves at the UTS
    rising_stress_curves = []
    falling_stress_curves = []

    rising_strain_curves = []
    falling_strain_curves = []

    for i, stresses in enumerate(stress_curves):
        # Calling split_at_UTS function
        [rising_stresses, relative_falling_stresses, rising_strains,
            relative_falling_strains] = split_at_uts(stresses, strain_curves[i])

        rising_stress_curves.append(rising_stresses)
        falling_stress_curves.append(relative_falling_stresses)

        rising_strain_curves.append(rising_strains)
        falling_strain_curves.append(relative_falling_strains)

    ''' Interpolating Average Rising Curve  - - - - - - - - - - - - - - - - '''
    [avg_rise_stress, avg_rise_strain] \
        = interpolate_avg_curve(avg_uts, num_element_rise,
                                rising_stress_curves, rising_strain_curves)

    ''' Interpolating Average Falling Curve  - - - - - - - - - - - - - - - '''
    # Slight preparation to get curve with relative changes
    rel_fall_stress_curves = []
    rel_fall_strain_curves = []
    for i in range(len(falling_stress_curves)):
        # Finding the UTS index
        uts_idx = np.argmax(stress_curves[i])
        ut_stress_value = stress_curves[i][uts_idx]
        ut_strain_value = strain_curves[i][uts_idx]

        relative_falling_stress = falling_stress_curves[i] - ut_stress_value
        rel_fall_stress_curves.append(relative_falling_stress)

        relative_falling_strain = falling_strain_curves[i] - ut_strain_value
        rel_fall_strain_curves.append(relative_falling_strain)

    # Function to interpolate the relative curves
    [rel_avg_fall_stress, rel_avg_fall_strain] \
        = interpolate_avg_curve(avg_stressdrop, num_element_fall,
                                rel_fall_stress_curves, rel_fall_strain_curves)

    # Additional processing - Going back to actual curve
    falling_stress_axis = rel_avg_fall_stress[0:-4] + avg_uts

    average_strain_curve_falling = (rel_avg_fall_strain[0:-4]
                                    + avg_rise_strain[-1])

    ''' Concatenating Curves for Graphing - - - - - - - - - - - - - - - - - '''
    average_stress_axis = (avg_rise_stress.tolist()
                           + falling_stress_axis.tolist())
    average_strain_axis = (avg_rise_strain.tolist()
                           + average_strain_curve_falling.tolist())

    ''' Plotting - Original Curves with Average Curve - - - - - - - - - - - '''
    # Establishing save paths first
    save_folder = "Average-Tensile-Graphs"
    simple_description = file_name.replace('_processed.csv', 'C')
    description = (simple_description.replace('C', '°C')
                   .replace('_', ' Filament at '))
    graph_description = f"Stress-Strain Curves for {description}"
    png_save_path = f"{save_folder}/{simple_description}.png"
    csv_save_path = f"{save_folder}/Average_{simple_description}.csv"

    plt.figure(figsize=(10, 6))

    # Plot original stress-strain curves
    for i in range(len(stress_curves)):
        plt.plot(strain_curves[i], stress_curves[i],
                 label=f"Test Curve {i+1}")

    # Plot the average rising curve
    plt.plot(average_strain_axis, average_stress_axis,
             label="Average Curve", linewidth=2, color="black", linestyle="--")

    # Labeling
    plt.title(graph_description)
    plt.xlabel("Strain")
    plt.ylabel("Stress [MPa]")
    plt.legend()
    plt.grid(True)

    ''' Save plot and average data points to a folder - - - - - - - - - - - '''
    plt.savefig(png_save_path, dpi=600)

    # Saving the average curve data points
    # Reshaping list to be a vertical array first
    average_stress = np.array(average_stress_axis).reshape(-1, 1)
    average_strain = np.array(average_strain_axis).reshape(-1, 1)

    average_data = pd.DataFrame(average_stress, columns=['Stress'])
    average_data['Strain'] = average_strain

    average_data.to_csv(csv_save_path, index=False)
    print(f"Saved results to: {csv_save_path}")

    # plt.show should go after saving the plot, because it clears it
    plt.show()
    # plt.close()



