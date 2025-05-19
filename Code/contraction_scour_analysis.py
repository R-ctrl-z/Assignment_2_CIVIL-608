"""
contraction_scour_analysis.py
This script analyzes contraction scour data from laboratory studies,
focusing on both clear-water and live-bed scour regimes.
It reads experimental data from a CSV file, computes relevant hydraulic and
sediment transport parameters, and applies several established contraction
scour equations (Straub 1934, Komura 1966, Gill 1981, Lim and Cheng 1998)
to predict flow depth at the contracted reach. The script then compares
measured and computed values for each study and visualizes the results
in a series of scatter plots.

Main functionalities:
- Reads and preprocesses contraction scour data from a CSV file.
- Filters data for clear-water and live-bed scour types.
- Calculates upstream Froude number, bed shear stress,
    and critical shear stress.
- Computes predicted contracted flow depths using multiple empirical equations
    for live-bed scour.
- Generates comparative scatter plots of measured vs. computed contracted flow
    depths for each model and study.
- Saves the resulting figure for reporting or publication.
Dependencies:
- pandas
- numpy
- matplotlib
- os
Raises:
- FileNotFoundError: If the specified CSV data file does not exist.

Author: Romain Van Mol
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set plotting defaults
plt.rcParams.update({
    "lines.linewidth": 1.5,
    "axes.labelsize": 12,
    "axes.titlesize": 16,
    "legend.fontsize": 16,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

# File path to CSV
csv_path = r"..\Data\CIVIL_608_Data.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at: {csv_path}")

# Import the data
contraction_table = pd.read_csv(csv_path)
contraction_table.columns = contraction_table.columns.str.strip()

# Physical parameters
g = 9.81           # [m/s^2] gravity
rho = 1000         # [kg/m^3] water density
theta_c = 0.047    # [-] critical Shield parameter

# Coefficient for Komura (1966) live-bed contraction scour equation
coeff_komura_live_bed = 1.45

# Filter the contraction table for clear-water and live-bed scour types
# Select rows for clear-water scour
clear_water = contraction_table["Type of scour"] == "clear-water"
clear_water_contraction_table = contraction_table[clear_water].copy()

# Select rows for live-bed scour
live_bed = contraction_table["Type of scour"] == "live-bed"
live_bed_contraction_table = contraction_table[live_bed].copy()

# Calculate upstream Froude number for clear-water cases
froude_upstream_clear_water = (
    clear_water_contraction_table["Upstream average flow velocity u1 [m/s]"] /
    np.sqrt(g * clear_water_contraction_table["Upstream flow depth y1 [m]"])
)
clear_water_contraction_table["froude_upstream"] = froude_upstream_clear_water

# Calculate upstream Froude number for live-bed cases
froude_upstream_live_bed = (
    live_bed_contraction_table["Upstream average flow velocity u1 [m/s]"] /
    np.sqrt(g * live_bed_contraction_table["Upstream flow depth y1 [m]"])
)
live_bed_contraction_table["froude_upstream"] = froude_upstream_live_bed

# Calculate bed shear stress (tau) for live-bed cases
tau_live_bed = (
    rho * g
    * live_bed_contraction_table[
        "Upstream average flow velocity u1 [m/s]"
    ] ** 2
    * (
        live_bed_contraction_table["Median diameter  [mm]"] / 1000
    ) ** (1/3)
    / (
        21.1 ** 2
        * live_bed_contraction_table["Upstream flow depth y1 [m]"] ** (1/3)
    )
)

# Calculate critical shear stress (tau_c) for live-bed cases
tau_c_live_bed = (
    theta_c * rho * g *
    (live_bed_contraction_table["Median diameter  [mm]"] / 1000) *
    (live_bed_contraction_table["Specific density"] - 1)
)

# Calculate ratio of bed shear stress to critical shear stress
ratio_tau_live_bed = tau_live_bed / tau_c_live_bed

# Add calculated values to the live-bed contraction table
live_bed_contraction_table["tau"] = tau_live_bed
live_bed_contraction_table["tau_c"] = tau_c_live_bed
live_bed_contraction_table["ratio_tau"] = ratio_tau_live_bed

# Identification of sub tables and scour depth equations for live-bed
authors_live_bed = [
    "Straub", "Ashida", "Komura", "Gill", "Rana", "Nowroozpour and Ettema"
]

# Dictionaries to store measured and computed y2 values for each study
live_bed_measured_y2_y1 = {}
live_bed_measured_y2 = {}
live_bed_computed = {}

# Loop through each live-bed contraction scour study
for study in authors_live_bed:
    study_key = study.replace(" ", "_")  # Key for dictionary (no spaces)
    # Filter the table for the current study
    study_filter = live_bed_contraction_table["Authors of the study"] == study
    study_table = live_bed_contraction_table[study_filter]

    # Store measured y2 values for the current study
    live_bed_measured_y2[study_key] = (
        study_table["Flow depth at contracted reach y2 [m]"].astype(float)
    )

    # Extract relevant columns for the current study
    ratioB2b1 = study_table["Ratio b2/b1"]
    tau = study_table["tau"]
    tau_c = study_table["tau_c"]
    y1 = study_table["Upstream flow depth y1 [m]"]
    geom_std = study_table["Geometric standard deviation"]
    froude = study_table["froude_upstream"]
    ratio_tau = study_table["ratio_tau"]

    # Compute predicted y2/y1 ratios using different live-bed
    # contraction scour equations
    with np.errstate(divide='ignore', invalid='ignore'):
        # Straub (1934) equation
        straub_1934 = (
            (1 / ratioB2b1) ** (6/7) *
            (tau_c / (2 * tau) + np.sqrt(
                (tau_c / (2 * tau)) ** 2 +
                (1 - tau_c / tau) * (1 / ratioB2b1)
            )) ** (-3/7)
        )
        y2_straub_1934 = straub_1934 * y1

        # Komura (1966) equation
        komura_1966 = (
            coeff_komura_live_bed * froude ** (1/5) *
            (1 / ratioB2b1) ** (2/3) *
            geom_std ** (-1/5)
        )
        y2_komura_1966 = komura_1966 * y1

        # Gill (1981) equation
        gill_1981 = (
            (1 / ratioB2b1) ** (6/7) *
            (
                (1 / ratioB2b1) ** (1/3) * (1 - (1 / ratio_tau)) +
                (1 / ratio_tau)
            ) ** (-3/7)
        )
        y2_gill_1981 = gill_1981 * y1

        # Lim and Cheng (1998) equation
        lim_cheng_1998 = (1 / ratioB2b1) ** 0.75
        y2_lim_cheng_1998 = lim_cheng_1998 * y1

    # Store computed y2 values for each model in a dictionary for this study
    live_bed_computed[study_key] = {
        "y2_Straub_1934": y2_straub_1934,
        "y2_Komura_1966": y2_komura_1966,
        "y2_Gill_1981": y2_gill_1981,
        "y2_Lim_Cheng_1998": y2_lim_cheng_1998,
    }

# Scour depth graphs live-bed

# Create a line for reference: y = x
# (perfect agreement between measured and computed)
x_line = np.linspace(0, 0.5, 100)
y_line = x_line

# Set up a 2x2 grid of subplots for the four models
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
plt.subplots_adjust(wspace=0.1, hspace=0.1)

# Define marker styles, colors, and labels for each study
markers = ['o', '+', 's', '^', 'x', 'D']
colors = ["#0072BD", "#D95319", "#EDB120", "#77AC30", "#7E2F8E", "#A2142F"]
labels = [
    'Straub (1934)', 'Ashida (1963)', 'Komura (1966)',
    'Gill (1981)', 'Rana (1986)', 'Nowroozpour and Ettema (2021)'
]

# Prepare study keys (replace spaces with underscores to match dictionary keys)
studies = [k.replace(" ", "_") for k in authors_live_bed]

# List of model keys and their titles for plotting
model_keys = [
    ("y2_Straub_1934", "Straub (1934)"),
    ("y2_Komura_1966", "Komura (1966)"),
    ("y2_Gill_1981", "Gill (1981)"),
    ("y2_Lim_Cheng_1998", "Lim and Cheng (1998)")
]

for ax, (model_key, model_title) in zip(axs.flat, model_keys):
    ax.plot(x_line, y_line, '-k', label='$Computed = Measured$')
    for i, study in enumerate(studies):
        y_measured = live_bed_measured_y2[study].values
        y_computed = live_bed_computed[study][model_key].values
        # Scatter plot of measured vs. computed y2 for each study
        ax.scatter(
            y_measured, y_computed,
            marker=markers[i],        # Marker style for each study
            color=colors[i],          # Color for each study
            label=labels[i],          # Legend label for each study
            s=60,                     # Marker size
            edgecolor='black',        # Marker edge color
            alpha=0.8                 # Marker transparency
        )
    # Set the title and axis labels for each subplot
    ax.set_title(model_title)
    ax.set_xlabel('Measured $y_{2}$ [m]')
    ax.set_ylabel('Computed $y_{2}$ [m]')
    ax.grid(True, linestyle='--', alpha=0.6)  # Add a grid for readability

# Set axis limits and aspect ratio for all subplots
for ax in axs.flat:
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    ax.set_aspect('equal', adjustable='box')  # Ensure 1:1 aspect ratio
    ax.autoscale(enable=False)  # Prevent autoscaling from changing limits

# Create a single legend for all subplots, placed below the plots
handles, legend_labels = axs[1, 1].get_legend_handles_labels()
fig.legend(
    handles,
    legend_labels,
    loc='lower center',
    ncol=3,
    bbox_to_anchor=(0.5, -0.03)
)
plt.tight_layout(rect=[0, 0.08, 1, 1])  # Adjust layout to fit legend
plt.show()  # Display the figure

# Save the figure to a file
fig.savefig(
    r"..\Figures\Scour_depth_live_bed.png",
    dpi=300, bbox_inches='tight', pad_inches=0.1
)
