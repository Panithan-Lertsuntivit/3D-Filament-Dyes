import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns  # Optional for a more polished plot

# Example data
colors = ["Red", "Blue", "Green", "Purple", "Black"]  # Qualitative axis (e.g., colors)
temperatures = [200, 215, 230]  # Quantitative axis (e.g., temperature in °C)

# Example values (stress data) for the heat map
stress_values = np.random.rand(len(colors), len(temperatures))  # Random stress data

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the pseudo-heatmap
cax = ax.imshow(stress_values, cmap="YlGnBu", aspect="auto")

# Add qualitative labels to the y-axis
ax.set_yticks(range(len(colors)))  # Positions for the qualitative labels
ax.set_yticklabels(colors)         # The qualitative labels

# Add quantitative labels to the x-axis
ax.set_xticks(range(len(temperatures)))  # Positions for temperature labels
ax.set_xticklabels(temperatures)         # The temperature values

# Add a colorbar to show the scale of the stress values
cbar = fig.colorbar(cax, ax=ax)
cbar.set_label("Stress [MPa]")

# Add axis labels and title
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Color")
ax.set_title("Pseudo Heatmap of Stress vs. Temperature and Color")

# Show the plot
plt.show()
