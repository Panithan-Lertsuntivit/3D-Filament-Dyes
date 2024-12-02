# Script is called Tensile-Part2-CurveAveraging.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

'''----- Beginning of Functions --------------------------------------------'''
def split_at_UTS(stress_values, strain_values):

    # Finding the UTS index
    UTS_idx = np.argmax(stress_values)

    # Splitting the arrays at the UTS (UTS value goes to rising trend)
    rising_stress = stress_values[0:UTS_idx+1]
    falling_stress = stress_values[UTS_idx: ]

    rising_strain = strain_values[0:UTS_idx+1]
    falling_strain = strain_values[UTS_idx: ]

    return rising_stress, falling_stress, rising_strain, falling_strain


'''----- End of Functions --------------------------------------------------'''

# Some testing of code first
file_location = f"Processed-Tensile-Data/Black_200_processed.csv"

df = pd.read_csv(file_location)
header_names = df.columns.tolist()
num_rows = len(df.index)

stress_curves = []
strain_curves = []

for i in range(num_rows):
    stress = df.loc[i, f'{header_names[1]}']
    strain = df.loc[i, f'{header_names[2]}']

    # Convert to string to list (ast.literal_eval) then convert to np array
    stress = np.array(ast.literal_eval(stress))
    strain = np.array(ast.literal_eval(strain))

    stress_curves.append(stress)
    strain_curves.append(strain)

# # Combining Curves
# stress_curves = [stress_1, stress_2, stress_3, stress_4]
# strain_curves = [strain_1, strain_2, strain_3, strain_4]


'''Plotting the original curves'''
# Plotting just the original curves
# Plotting
plt.figure(figsize=(10, 6))

# Plot original stress-strain curves
for i in range(len(stress_curves)):
    plt.plot(strain_curves[i], stress_curves[i], label=f"Trial {i+1} Curve")

plt.title("Stress-Strain Curves")
plt.xlabel("Strain")
plt.ylabel("Stress [MPa]")
plt.legend()
plt.grid(True)
plt.show()

'''End of plotting the original curves'''

# Splitting stress/strain curves at the UTS and finding the average UTS
rising_stress_curves = []
falling_stress_curves = []

rising_strain_curves = []
falling_strain_curves = []

uts_values = []
num_rising_elements = 0
num_falling_elements = 0

for i, stresses in enumerate(stress_curves):
    uts_values.append(max(stresses))

    # Calling split_at_UTS function
    [rising_stresses, falling_stresses, rising_strains,
        falling_strains] = split_at_UTS(stresses, strain_curves[i])

    if len(rising_stresses) > num_rising_elements:
        num_rising_elements = len(rising_stresses)

    if len(falling_stresses) > num_falling_elements:
        num_falling_elements = len(falling_stresses)

    rising_stress_curves.append(rising_stresses)
    falling_stress_curves.append(falling_stresses)

    rising_strain_curves.append(rising_strains)
    falling_strain_curves.append(falling_strains)

average_uts = np.mean(uts_values)
# print(average_uts)
# curve = np.array(rising_stress_curves[0])
# print(curve)

# Interpolation for the rising curves up to the average uts
rising_stress_axis = np.linspace(0, average_uts, 2*num_rising_elements)

interpolated_strain_axes = []
for i in range(len(rising_stress_curves)):
    interpolated_strains = np.interp(rising_stress_axis, rising_stress_curves[i], rising_strain_curves[i])
    interpolated_strain_axes.append(interpolated_strains)

average_strain_curve = np.mean(interpolated_strain_axes, axis=0)

print(average_strain_curve)

# Plotting
plt.figure(figsize=(10, 6))

# Plot original stress-strain curves
for i in range(len(stress_curves)):
    plt.plot(strain_curves[i], stress_curves[i], label=f"Trial {i+1} Curve")

# Plot the average rising curve
plt.plot(average_strain_curve, rising_stress_axis, label="Average Curve (Rising)", linewidth=2, color="black", linestyle="--")

# Labeling
plt.title("Stress-Strain Curves and Average Curve")
plt.xlabel("Strain")
plt.ylabel("Stress [MPa]")
plt.legend()
plt.grid(True)
plt.show()