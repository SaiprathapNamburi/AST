import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV file
file_path = "data/comparison.csv"

try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found!")
    exit()

# Extract values
playstore_values = data[data["Type"] == "Playstore"].iloc[:, 1:].values.flatten()
release_values = data[data["Type"] == "Release"].iloc[:, 1:].values.flatten()

# Compute differences
differences = release_values - playstore_values

# Define categories
categories = ["Splash (ms)", "Onboarding (ms)", "Home (ms)"]

# Define scaling factor to reduce bar height
scaling_factor = 0.5  # Adjust this to control bar height

# Apply scaling factor
scaled_playstore_values = playstore_values * scaling_factor
scaled_release_values = release_values * scaling_factor

# Define bar width and X positions
bar_width = 0.3  # Adjusted bar width for better spacing
x = np.arange(len(categories))

# Create the plot
plt.figure(figsize=(10, 6))  # Increased figure size

# Iterate through categories to assign colors dynamically
for i in range(len(categories)):
    if differences[i] > 0:  # Release is greater -> Release (red), Playstore (green)
        playstore_color = "green"
        release_color = "red"
        diff_color = "red"
    else:  # Playstore is greater -> Release (green), Playstore (red)
        playstore_color = "red"
        release_color = "green"
        diff_color = "green"

    # Plot bars with reduced height
    plt.bar(x[i] - bar_width/2, scaled_playstore_values[i], bar_width, color=playstore_color, label="Playstore" if i == 0 else "")
    plt.bar(x[i] + bar_width/2, scaled_release_values[i], bar_width, color=release_color, label="Release" if i == 0 else "")

    # Add values on top of bars
    plt.text(x[i] - bar_width/2, scaled_playstore_values[i] + 5, f"{playstore_values[i]:.1f}", 
             ha="center", fontsize=10, fontweight="bold", color="black")
    plt.text(x[i] + bar_width/2, scaled_release_values[i] + 5, f"{release_values[i]:.1f}", 
             ha="center", fontsize=10, fontweight="bold", color="black")

# Add difference values BELOW the category labels
for i in range(len(categories)):
    diff_color = "red" if differences[i] >= 0 else "green"  # Set color dynamically
    diff_text = f"Δ {differences[i]:.0f} ms"  # Difference text (Δ symbol for clarity)
    
    plt.text(x[i], -max(scaled_playstore_values) * 0.2, diff_text, 
             ha="center", fontsize=11, fontweight="bold", color=diff_color)

# Add labels
plt.xlabel("Activity Type", fontsize=12, fontweight="bold")
plt.ylabel("App Start Time (ms)", fontsize=12, fontweight="bold")
plt.title("Comparison of App Start Time: Playstore vs Release", fontsize=14, fontweight="bold")
plt.xticks(x, categories, fontsize=11)

# # Add legend
# plt.legend(loc="upper right")

# Adjust Y-axis limits to prevent overlap
plt.ylim(-max(scaled_playstore_values) * 0.3, max(max(scaled_playstore_values), max(scaled_release_values)) + 20)

# Save and display graph
output_path = "data/app_start_time_comparison_fixed.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Graph saved successfully at: {output_path}")

plt.show()
