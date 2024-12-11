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
                    y_label, y_start):
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
    plt.legend(title="Categories")

    # Show plot
    plt.tight_layout()
    plt.show()


''' End of Functions '''


# Order of Groups
grouping_order = np.array([
    # Temperature of 200C
    ['Red_200', 'Green_200', 'Blue_200', 'Purple_200', 'Black_200'],
    # Temperature of 215C
    ['Red_215', 'Green_215', 'Blue_215', 'Purple_215', 'Black_215'],
    # Temperature of 230C
    ['Red_230', 'Green_230', 'Blue_230', 'Purple_230', 'Black_230']
])

# Extracting Data from csv file
csv_path = "Tensile-Results/Table_Categories.csv"
avg_values = pd.read_csv(csv_path)

# Data Labels
colors = ['Red', 'Green', 'Blue', 'Purple', 'Black']        # X-axis labels
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


bargraph_result(avg_uts, std_uts, colors, temperatures,
                "Ultimate Tensile Strength [MPa]", 25)

bargraph_result(avg_youngmodulus, std_youngmodulus, colors, temperatures,
                "Young's Modulus [MPa]", 0)

bargraph_result(avg_yieldstrength, std_yieldstrength, colors, temperatures,
                "Yield Strength [MPa]", 0)