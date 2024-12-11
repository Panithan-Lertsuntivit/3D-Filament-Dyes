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

def bargraph_result(avg_values, std_values, color_label, temp_label,
                    y_label, y_start, save_path):
    # Bar Graph Settings
    x = np.arange(len(color_label))  # X positions for the bars
    width = 0.2             # Width of each bar
    spacing = 0.05          # Extra spacing between bars within each group
    bar_colors = ['cornflowerblue', 'coral', 'mediumseagreen']

    # Plot each category
    for i, (temp_num, bar_color) in enumerate(zip(temp_label, bar_colors)):
        # Adjust bar positions with spacing
        bar_positions = x + i * (width + spacing)
        plt.bar(bar_positions, avg_values[i], yerr=std_values[i], capsize=5,
                width=width, label=temp_num, color=bar_color, alpha=0.8)

    # Add labels and title
    plt.xticks(x + (width + spacing) * (len(temp_label) - 1) / 2,
               color_label)  # Center the x-axis ticks
    plt.ylim(bottom=y_start)
    plt.xlabel('Temperature')
    plt.ylabel(f'{y_label}')
    plt.title(f'Bar Graph Comparison of Average {y_label}')
    plt.legend(title="Temperatures", facecolor="white", edgecolor="black",
               framealpha=1.0, loc='lower left')

    # Show plot
    plt.tight_layout()
    plt.savefig(save_path, dpi=600)
    print(f"Saved bar graph to: {save_path}")

    plt.show()


''' End of Functions '''

# Order of Groups
grouping_order = np.array([
    # Temperature of 200C
    ['Black_200', 'Blue_200', 'Green_200', 'Purple_200', 'Red_200'],
    # Temperature of 215C
    ['Black_215', 'Blue_215', 'Green_215', 'Purple_215', 'Red_215'],
    # Temperature of 230C
    ['Black_230', 'Blue_230', 'Green_230', 'Purple_230', 'Red_230']
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

bargraph_result(avg_flexmodulus, std_flexmodulus, colors, temperatures,
                "Flexural Modulus [MPa]",
                1.3, save_path_flex_modulus)

bargraph_result(avg_flex_yieldstrength, std_flex_yieldstrength,
                colors, temperatures,
                "Flexural Yield Strength [MPa]",
                0.018, save_path_flex_yieldstrength)