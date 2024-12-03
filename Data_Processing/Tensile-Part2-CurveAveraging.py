# Script is called Tensile-Part2-CurveAveraging.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

'''----- Beginning of Functions --------------------------------------------'''
def stress_strain_from_csv(filelocation):

    array_stresses = []
    array_strains = []

    data_frame = pd.read_csv(filelocation)
    header_names = data_frame.columns.tolist()
    num_rows = len(data_frame.index)

    for j in range(num_rows):
        stress = data_frame.loc[j, f'{header_names[1]}']
        strain = data_frame.loc[j, f'{header_names[2]}']

        # Convert to string to list (ast.literal_eval) then convert to np array
        stress = np.array(ast.literal_eval(stress))
        strain = np.array(ast.literal_eval(strain))

        array_stresses.append(stress)
        array_strains.append(strain)

    return array_stresses, array_strains

def split_at_UTS(stress_values, strain_values):

    # Finding the UTS index
    UTS_idx = np.argmax(stress_values)

    # Splitting the arrays at the UTS (UTS value goes to rising trend)
    rising_stress = stress_values[0:UTS_idx+1]
    falling_stress = stress_values[UTS_idx+2: ]

    rising_strain = strain_values[0:UTS_idx+1]
    falling_strain = strain_values[UTS_idx+2: ]

    # Need to output relative falling stress/strain
    relative_falling_stress = falling_stress - rising_stress[-1]
    relative_falling_strain = falling_strain - rising_strain[-1]

    return (rising_stress, relative_falling_stress, rising_strain,
            relative_falling_strain)


'''----- End of Functions --------------------------------------------------'''

# Some testing of code first
file_location = f"Processed-Tensile-Data/Black_230_processed.csv"

''' Call function to read data from csv file to get stress and strain curves '''
[stress_curves, strain_curves] = stress_strain_from_csv(file_location)

''' Splitting the stress/strain curves at the UTS ------------------------'''
# Splitting stress/strain curves at the UTS and finding the average UTS
rising_stress_curves = []
relative_falling_stress_curves = []

rising_strain_curves = []
relative_falling_strain_curves = []

uts_values = []
num_rising_elements = 0
num_falling_elements = 0
stress_drops_after_UTS = []

for i, stresses in enumerate(stress_curves):
    uts_values.append(max(stresses))

    # Calling split_at_UTS function
    [rising_stresses, relative_falling_stresses, rising_strains,
        relative_falling_strains] = split_at_UTS(stresses, strain_curves[i])

    # Keeping track of elements
    if len(rising_stresses) > num_rising_elements:
        num_rising_elements = len(rising_stresses)

    if len(relative_falling_stresses) > num_falling_elements:
        num_falling_elements = len(relative_falling_stresses)

    current_stress_drop = relative_falling_stresses[-1]
    stress_drops_after_UTS.append(current_stress_drop)

    rising_stress_curves.append(rising_stresses)
    relative_falling_stress_curves.append(relative_falling_stresses)

    rising_strain_curves.append(rising_strains)
    relative_falling_strain_curves.append(relative_falling_strains)

# Calculating Averages - Used in interpolation
average_uts = np.mean(uts_values)
average_stress_drop = np.mean(stress_drops_after_UTS)

''' Interpolation of the rising curve up to the UTS -------------------'''
# Interpolation for the rising curves up to the average uts
rising_stress_axis = np.linspace(0, average_uts, num_rising_elements)

interpolated_strain_axes_rising = []
for i in range(len(rising_stress_curves)):
    interpolated_strains_rising = np.interp(rising_stress_axis,
                                            rising_stress_curves[i],
                                            rising_strain_curves[i])
    interpolated_strain_axes_rising.append(interpolated_strains_rising)

average_strain_curve_rising = np.mean(interpolated_strain_axes_rising, axis=0)

''' Interpolation of the relative falling curve after UTS ------------------'''
relative_falling_stress_axis = np.linspace(0, average_stress_drop,
                                           num_falling_elements)

interpolated_strain_axes_falling = []
for i in range(len(relative_falling_stress_curves)):
    interpolated_strains_falling = np.interp(relative_falling_stress_axis,
                                             relative_falling_stress_curves[i],
                                             relative_falling_strain_curves[i])
    interpolated_strain_axes_falling.append(interpolated_strains_falling)

relative_average_strain_curve_falling \
    = np.mean(interpolated_strain_axes_falling, axis=0)

falling_stress_axis = relative_falling_stress_axis[0:-2] + average_uts

average_strain_curve_falling = (relative_average_strain_curve_falling[0:-2] +
                                average_strain_curve_rising[-1])

''' Preparing to plot average curve - ---------------------------------'''
average_stress_axis = rising_stress_axis.tolist() + falling_stress_axis.tolist()
average_strain_axis = (average_strain_curve_rising.tolist()
                       + average_strain_curve_falling.tolist())

''' Plotting the original curves with the average curve ----------------'''
# Plotting
plt.figure(figsize=(10, 6))

# Plot original stress-strain curves
for i in range(len(stress_curves)):
    plt.plot(strain_curves[i], stress_curves[i], label=f"Test Curve {i+1}")

# Plot the average rising curve
plt.plot(average_strain_axis, average_stress_axis,
         label="Average Curve", linewidth=2, color="black", linestyle="--")

# Labeling
plt.title("Stress-Strain Curves and Average Curve")
plt.xlabel("Strain")
plt.ylabel("Stress [MPa]")
plt.legend()
plt.grid(True)
plt.show()

''' End of Plotting -----------------------------------------------------'''
