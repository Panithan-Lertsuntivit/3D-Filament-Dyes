# Script is called Tensile-Part2-CurveAveraging.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

stress_1 = df[f'{header_names[0]}'].to_numpy()
strain_1 = df[f'{header_names[1]}'].to_numpy()

stress_2 = df[f'{header_names[2]}'].to_numpy()
strain_2 = df[f'{header_names[3]}'].to_numpy()

stress_3 = df[f'{header_names[4]}'].to_numpy()
strain_3 = df[f'{header_names[5]}'].to_numpy()

stress_4 = df[f'{header_names[6]}'].to_numpy()
strain_4 = df[f'{header_names[7]}'].to_numpy()

# Combining Curves
stress_curves = [stress_1, stress_2, stress_3, stress_4]
strain_curves = [strain_1, strain_2, strain_3, strain_4]

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
print(average_uts)
curve = np.array(rising_stress_curves[0])
print(curve)

# Interpolation for the rising curves
rising_stress_axis = np.linspace(0, average_uts, 2*num_rising_elements)

# # Next
# aligned_strains_curves = []
# for i in range(len(stress_curves)):
#     aligned_strains = np.interp(common_stress_axis, stress_curves[i], strain_curves[i])
#     aligned_strains_curves.append(aligned_strains)

