# Script is called Tensile-Part6-BarGraph.py
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

    # Initializing a figure
    plt.figure(figsize=(8, 6))
    title_size = 13.5
    label_size = 12
    tick_size = 11.5

    # Plot each category
    for i, (temp_num, bar_color) in enumerate(zip(temp_label, bar_colors)):
        # Adjust bar positions with spacing
        bar_positions = x + i * (width + spacing)
        plt.bar(bar_positions, avg_values[i], yerr=std_values[i], capsize=5,
                width=width, label=temp_num, color=bar_color, alpha=0.8)

    # Add labels and title
    plt.xticks(x + (width + spacing) * (len(temp_label) - 1) / 2,
               color_label, fontsize=tick_size)  # Center the x-axis ticks
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
    # Temperature of 200C
    ['Black_200', 'Blue_200', 'Green_200', 'Purple_200', 'Red_200'],
    # Temperature of 215C
    ['Black_215', 'Blue_215', 'Green_215', 'Purple_215', 'Red_215'],
    # Temperature of 230C
    ['Black_230', 'Blue_230', 'Green_230', 'Purple_230', 'Red_230']
])

# Extracting Data from csv file
csv_path = "Tensile-Results/Table_Categories.csv"
avg_values = pd.read_csv(csv_path)

# Data Labels
colors = ['Black', 'Blue', 'Green', 'Purple', 'Red']        # X-axis labels
temperatures = ['200°C', '215°C', '230°C']                  # Y-axis labels


# Collecting Data
[avg_uts, std_uts] \
    = collect_from_pandas_dataframe(avg_values, grouping_order,
                                    'AVG_UTS', 'STD_UTS')
[avg_youngmodulus, std_youngmodulus] \
    = collect_from_pandas_dataframe(avg_values, grouping_order,
                                    'AVG_YoungModulus', 'STD_YoungModulus')
[avg_yieldstrength, std_yieldstrength] \
    = collect_from_pandas_dataframe(avg_values, grouping_order,
                                    'AVG_Yield_Strength', 'STD_Yield_Strength')

# Making Save Paths
save_path_uts = "Tensile-Results/BarGraph_UTS.png"
save_path_youngmodulus = "Tensile-Results/BarGraph_YoungModulus.png"
save_path_yieldstrength = "Tensile-Results/BarGraph_YieldStrength.png"


bargraph_result(avg_uts, std_uts, colors, temperatures,
                "Ultimate Tensile Strength [MPa]",
                38, save_path_uts)

bargraph_result(avg_youngmodulus, std_youngmodulus, colors, temperatures,
                "Young's Modulus [MPa]",
                750, save_path_youngmodulus)

bargraph_result(avg_yieldstrength, std_yieldstrength, colors, temperatures,
                "Yield Strength [MPa]",
                8, save_path_yieldstrength)