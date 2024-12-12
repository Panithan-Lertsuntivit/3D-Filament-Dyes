# Script is called 3Point-Part5-BarGraph.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

''' Beginning of Functions '''
def collect_from_pandas_dataframe(data_frame, order_groups, avg_label, std_label):
    # Size of order of groups
    [rows, columns] = order_groups.shape

    # Predefining numpy arrays
    avg = np.zeros((rows, columns))
    std = np.zeros((rows, columns))

    for i in range(rows):
        for j in range(columns):
            avg[i, j] = data_frame.loc[data_frame['Category']
                                       == order_groups[i, j], avg_label].iloc[0]
            std[i, j] = data_frame.loc[data_frame['Category']
                                       == order_groups[i, j], std_label].iloc[0]

    return avg, std

def bargraph_result(avg_values, std_values, x_tick_labels, legend_labels,
                    y_label, y_start, save_path):
    # Bar Graph Settings
    x = np.arange(len(x_tick_labels))  # X positions for the bars
    width = 0.145            # Width of each bar
    spacing = 0.025          # Extra spacing between bars within each group
    bar_colors = ['gray', 'cornflowerblue', 'mediumseagreen',
                  'mediumpurple', 'coral']

    # Initializing a figure
    plt.figure(figsize=(8, 6))
    title_size = 13.5
    label_size = 12
    tick_size = 11.5

    # Plot each category
    for i, (temp_num, bar_color) in enumerate(zip(legend_labels, bar_colors)):
        # Adjust bar positions with spacing
        bar_positions = x + i * (width + spacing)
        plt.bar(bar_positions, avg_values[i], yerr=std_values[i], capsize=5,
                width=width, label=temp_num, color=bar_color, alpha=0.8)

    # Add labels and title
    plt.xticks(x + (width + spacing) * (len(legend_labels) - 1) / 2,
               x_tick_labels, fontsize=tick_size)  # Center the x-axis ticks
    plt.ylim(bottom=y_start)
    plt.xlabel('Temperature', fontsize=label_size)
    plt.ylabel(f'{y_label}', fontsize=label_size)
    plt.title(f'Bar Graph Comparison of Average {y_label}',
              fontsize=title_size, fontweight='bold')

    # Tick Marks and Legend
    # Adjust tick parameters
    plt.tick_params(axis='both', which='major', labelsize=tick_size)
    plt.legend(title="Temperatures", facecolor="white", edgecolor="black",
               framealpha=1.0, loc='lower left',
               fontsize=label_size, title_fontsize=title_size)

    # Show plot
    plt.tight_layout()
    plt.savefig(save_path, dpi=600)
    print(f"Saved bar graph to: {save_path}")

    plt.show()


''' End of Functions '''

# Order of Groups
grouping_order = np.array([
    # Black Filament
    ['Black_200', 'Black_215', 'Black_230'],
    # Blue Filament
    ['Blue_200', 'Blue_215', 'Blue_230'],
    # Green Filament
    ['Green_200', 'Green_215', 'Green_230'],
    # Purple Filament
    ['Purple_200', 'Purple_215', 'Purple_230'],
    # Red Filament
    ['Red_200', 'Red_215', 'Red_230'],
])

# Extracting Data from csv file
csv_path = "3Point-Results/Table_Flex_Categories.csv"
avg_values = pd.read_csv(csv_path)

# Data Labels
colors = ['Black', 'Blue', 'Green', 'Purple', 'Red']        # X-axis labels
temperatures = ['200°C', '215°C', '230°C']                  # Y-axis labels

# Collecting Data
[avg_flexmodulus, std_flexmodulus] \
    = collect_from_pandas_dataframe(avg_values, grouping_order,
                                    'AVG_FlexModulus',
                                    'STD_FlexModulus')
[avg_flex_yieldstrength, std_flex_yieldstrength] \
    = collect_from_pandas_dataframe(avg_values, grouping_order,
                                    'AVG_FlexYield_Strength',
                                    'STD_FlexYield_Strength')

# Making Save Paths and then bar graphs
save_path_flex_modulus = "3Point-Results/BarGraph_FlexModulus.png"
save_path_flex_yieldstrength = "3Point-Results/BarGraph_Flex_YieldStrength.png"

bargraph_result(avg_flexmodulus, std_flexmodulus, temperatures, colors,
                "Flexural Modulus [MPa]",
                1.3, save_path_flex_modulus)

bargraph_result(avg_flex_yieldstrength, std_flex_yieldstrength,
                temperatures, colors,
                "Flexural Yield Strength [MPa]",
                0.018, save_path_flex_yieldstrength)