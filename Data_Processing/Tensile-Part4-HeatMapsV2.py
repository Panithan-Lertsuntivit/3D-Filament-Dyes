import matplotlib.pyplot as plt
import numpy as np

# Example data: Mean stress and standard deviation for each color-temperature combination
colors = ['Black', 'Purple', 'Green', 'Blue', 'Red']
temperatures = [200, 215, 230]

mean_stress = np.array([
    [75, 60, 50],  # Black
    [65, 55, 45],  # Purple
    [35, 40, 50],  # Green
    [40, 45, 55],  # Blue
    [30, 35, 50]   # Red
])

std_dev = np.array([
    [5, 3, 4],  # Black
    [4, 2, 3],  # Purple
    [2, 2, 2],  # Green
    [3, 3, 4],  # Blue
    [3, 4, 5]   # Red
])

# Normalize circle sizes for visibility
circle_sizes = (std_dev / std_dev.max()) * 1000

# Create figure and axis
fig, ax = plt.subplots(figsize=(6, 6))

# Plot circles for each data point
for i, color in enumerate(colors):
    for j, temp in enumerate(temperatures):
        ax.scatter(
            j, i, s=circle_sizes[i, j],
            c=mean_stress[i, j], cmap='YlGnBu',
            vmin=mean_stress.min(), vmax=mean_stress.max()
        )

# Add colorbar
cbar = plt.colorbar(ax.collections[0], ax=ax)
cbar.set_label('Mean Stress [MPa]')

# Set axis labels
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Color')

# Adjust tick positions and labels
ax.set_xticks(range(len(temperatures)))
ax.set_xticklabels(temperatures)

ax.set_yticks(range(len(colors)))
ax.set_yticklabels(colors)

# Adjust axis limits to reduce spacing
ax.set_xlim(-0.3, len(temperatures) - 0.7)  # Reduce horizontal spacing
ax.set_ylim(-0.3, len(colors) - 0.7)        # Reduce vertical spacing

# Add a title
ax.set_title('Circle-Based Pseudo Heatmap of Stress (Circle Size = Std. Dev.)')

# Optimize layout
plt.tight_layout()
plt.show()