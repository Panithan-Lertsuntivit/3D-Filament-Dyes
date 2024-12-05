import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

''' - - - - - Beginning of Functions - - - - - - - - - - - - - - - - - - - '''

def dataframe_heatmap_array(value_data_frame, std_data_frame, num_x, num_y):
    # Convert Data Frame to np array for heat map graphing
    values = value_data_frame.to_numpy()
    std = std_data_frame.to_numpy()

    # Initialize numpy arrays and counter
    value_array = np.zeros((num_y, num_x))
    std_array = np.zeros((num_y, num_x))
    counter = 0

    # For Loop
    for y in range(num_y):
        for x in range(num_x):
            value_array[y, x] = values[counter]
            std_array[y, x] = std[counter]
            counter = counter + 1

    return value_array, std_array


def circle_heatmap(magnitude_array, std_array, x_axis, y_axis,
                   name, description):
    # Normalize circle sizes for visibility
    circle_scaling = 4000
    circle_magnitudes = (std_array / std_array.max()) * circle_scaling

    # Create figure and axis
    fig_x_length = 8
    fig_y_length = 9
    [fig, ax] = plt.subplots(figsize=(fig_x_length, fig_y_length))

    # Plot circles for each data point
    for i, color in enumerate(y_axis):
        for j, temp in enumerate(x_axis):
            ax.scatter(
                j, i, s=circle_magnitudes[i, j], c=magnitude_array[i, j],
                cmap='copper', vmin=magnitude_array.min(),
                vmax=magnitude_array.max()
            )

    # Add colorbar
    cbar = plt.colorbar(ax.collections[0], ax=ax)
    colorbar_description = f'{description}'
    # cbar.set_label('Ultimate Tensile Strength [MPa]')
    cbar.set_label(colorbar_description)

    # Set axis labels
    ax.set_xlabel('Temperature [°C]')
    ax.set_ylabel('Color')

    # Adjust tick positions and labels
    ax.set_xticks(range(len(temperatures)))
    ax.set_xticklabels(temperatures)

    ax.set_yticks(range(len(colors)))
    ax.set_yticklabels(colors)

    # Adjust axis limits to reduce spacing
    x_axis_offset = -0.5
    x_axis_spacing = len(temperatures) + x_axis_offset

    y_axis_offset = -0.5
    y_axis_spacing = len(colors) + y_axis_offset

    ax.set_xlim(x_axis_offset, x_axis_spacing)
    ax.set_ylim(y_axis_offset, y_axis_spacing)

    # Add a title
    title = f'Circle-Based Heatmap for {name}'
    ax.set_title(title)

    # Optimize layout and save before showing
    plt.tight_layout()

    png_save_path = f'Tensile-Results/Heatmap_{name}.png'
    plt.savefig(png_save_path, dpi=600)
    print(f"Saved plot to: {png_save_path}")

    plt.show()


''' - - - - - End of Functions - - - - - - - - - - - - - - - - - - - '''


# Example data: Mean stress and standard deviation for each color-temperature combination
colors = ['Red', 'Blue', 'Green', 'Purple', 'Black']
temperatures = [200, 215, 230]

file_path = 'Tensile-Results/Table_Categories.csv'

# Creating pandas DataFrames to read csv, and save average/std values
csv_readings = pd.read_csv(file_path)
header_names = csv_readings.columns.tolist()
mean_values = pd.DataFrame()
std_values = pd.DataFrame()

avg_columns = [f'{header_names[1]}', f'{header_names[2]}', f'{header_names[3]}']
std_columns = [f'{header_names[4]}', f'{header_names[5]}', f'{header_names[6]}']

# DataFrame for average or mean values
mean_values['Category'] = csv_readings[f'{header_names[0]}']
mean_values[['UTS', 'YoungModulus', 'Toughness']] = csv_readings[avg_columns]

std_values['Category'] = csv_readings[f'{header_names[0]}']
std_values[['UTS', 'YoungModulus', 'Toughness']] = csv_readings[std_columns]


''' ------- '''
num_colors = len(colors)
num_temps = len(temperatures)

[avg_uts, std_uts] \
    = dataframe_heatmap_array(mean_values['UTS'], std_values['UTS'],
                              num_temps, num_colors)

[avg_youngmodulus, std_youngmodulus] \
    = dataframe_heatmap_array(mean_values['YoungModulus'],
                              std_values['YoungModulus'], num_temps, num_colors)

[avg_tough, std_tough] \
    = dataframe_heatmap_array(mean_values['Toughness'],
                              std_values['Toughness'], num_temps, num_colors)

circle_heatmap(avg_uts, std_uts, temperatures, colors,
               'UTS', 'Ultimate Tensile Stress [MPa]')
circle_heatmap(avg_youngmodulus, std_youngmodulus, temperatures, colors,
               "Young's Modulus", "Young's Modulus [MPa]")
circle_heatmap(avg_tough, std_tough, temperatures, colors,
               'Toughness', 'Toughness [J/m^3]')


# mean_stress = avg_uts
# std_dev = std_uts
#
# # mean_stress = np.array([
# #     [75, 60, 50],  # Black
# #     [65, 55, 45],  # Purple
# #     [35, 40, 50],  # Green
# #     [40, 45, 55],  # Blue
# #     [30, 35, 50]   # Red
# # ])
# #
# # std_dev = np.array([
# #     [5, 3, 4],  # Black
# #     [4, 2, 3],  # Purple
# #     [2, 2, 2],  # Green
# #     [3, 3, 4],  # Blue
# #     [3, 4, 5]   # Red
# # ])
#
# # Normalize circle sizes for visibility
# circle_scale_factor = 4000
# circle_sizes = (std_dev / std_dev.max()) * circle_scale_factor
#
# # Create figure and axis
# fig_x_length = 8
# fig_y_length = 9
# fig, ax = plt.subplots(figsize=(fig_x_length, fig_y_length))
#
# # Plot circles for each data point
# for i, color in enumerate(colors):
#     for j, temp in enumerate(temperatures):
#         ax.scatter(
#             j, i, s=circle_sizes[i, j],
#             c=mean_stress[i, j], cmap='copper',
#             vmin=mean_stress.min(), vmax=mean_stress.max()
#         )
#
# # Add colorbar
# cbar = plt.colorbar(ax.collections[0], ax=ax)
# cbar.set_label('Ultimate Tensile Strength [MPa]')
#
# # Set axis labels
# ax.set_xlabel('Temperature [°C]')
# ax.set_ylabel('Color')
#
# # Adjust tick positions and labels
# ax.set_xticks(range(len(temperatures)))
# ax.set_xticklabels(temperatures)
#
# ax.set_yticks(range(len(colors)))
# ax.set_yticklabels(colors)
#
# # Adjust axis limits to reduce spacing
# x_axis_offset = -0.5
# x_axis_spacing = len(temperatures) + x_axis_offset
#
# y_axis_offset = -0.5
# y_axis_spacing = len(colors) + y_axis_offset
#
# ax.set_xlim(x_axis_offset, x_axis_spacing)
# ax.set_ylim(y_axis_offset, y_axis_spacing)
#
# # Add a title
# ax.set_title('Circle-Based Heatmap of UTS')
#
# # Optimize layout
# plt.tight_layout()
# plt.show()