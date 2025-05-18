import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set plotting defaults
""" plt.rcParams.update({
    "lines.linewidth": 1.5,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "text.usetex": True,
}) """

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

# Median diameter distribution
clear_water = contraction_table["Type of scour"] == "clear-water"
clear_water_contraction_table = contraction_table[clear_water].copy()

live_bed = contraction_table["Type of scour"] == "live-bed"
live_bed_contraction_table = contraction_table[live_bed].copy()

# Froude number
froude_upstream_clear_water = (
    clear_water_contraction_table["Upstream average flow velocity u1 [m/s]"] /
    np.sqrt(g * clear_water_contraction_table["Upstream flow depth y1 [m]"])
)
clear_water_contraction_table["froude_upstream"] = froude_upstream_clear_water

edges_froude_upstream = np.array([0, 0.14, 0.28, 0.42, 0.56, 0.70, 0.84, 98])
edges_froude_upstream[1:-1] += np.finfo(float).eps
froude_upstream_clear_water_hist = np.histogram(
    froude_upstream_clear_water, bins=edges_froude_upstream
)[0]

froude_upstream_live_bed = (
    live_bed_contraction_table["Upstream average flow velocity u1 [m/s]"] /
    np.sqrt(g * live_bed_contraction_table["Upstream flow depth y1 [m]"])
)
live_bed_contraction_table["froude_upstream"] = froude_upstream_live_bed
froude_upstream_live_bed_hist = np.histogram(
    froude_upstream_live_bed, bins=edges_froude_upstream
)[0]

# Shear stress ratio (live-bed)
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
tau_c_live_bed = (
    theta_c * rho * g *
    (live_bed_contraction_table["Median diameter  [mm]"] / 1000) *
    (live_bed_contraction_table["Specific density"] - 1)
)
ratio_tau_live_bed = tau_live_bed / tau_c_live_bed
live_bed_contraction_table["tau"] = tau_live_bed
live_bed_contraction_table["tau_c"] = tau_c_live_bed
live_bed_contraction_table["ratio_tau"] = ratio_tau_live_bed

# Identification of sub tables and scour depth equations for live-bed
authors_live_bed = [
    "Straub", "Ashida", "Komura", "Gill", "Rana", "Nowroozpour and Ettema"
]
coeff_komura_live_bed = 1.45

live_bed_measured_y2_y1 = {}
live_bed_measured_y2 = {}
live_bed_computed = {}

for study in authors_live_bed:
    study_key = study.replace(" ", "_")
    study_filter = live_bed_contraction_table["Authors of the study"] == study
    study_table = live_bed_contraction_table[study_filter]

    # Measured values
    live_bed_measured_y2[study_key] = (
        study_table["Flow depth at contracted reach y2 [m]"].astype(float)
    )

    # Computed values for Straub (1934)
    ratioB2b1 = study_table["Ratio b2/b1"]
    tau = study_table["tau"]
    tau_c = study_table["tau_c"]
    y1 = study_table["Upstream flow depth y1 [m]"]
    geom_std = study_table["Geometric standard deviation"]
    froude = study_table["froude_upstream"]
    ratio_tau = study_table["ratio_tau"]

    with np.errstate(divide='ignore', invalid='ignore'):
        straub_1934 = (
            (1 / ratioB2b1) ** (6/7) *
            (tau_c / (2 * tau) + np.sqrt(
                (tau_c / (2 * tau)) ** 2 +
                (1 - tau_c / tau) * (1 / ratioB2b1)
            )) ** (-3/7)
        )
        y2_straub_1934 = straub_1934 * y1

        komura_1966 = (
            coeff_komura_live_bed * froude ** (1/5) *
            (1 / ratioB2b1) ** (2/3) *
            geom_std ** (-1/5)
        )
        y2_komura_1966 = komura_1966 * y1

        gill_1981 = (
            (1 / ratioB2b1) ** (6/7) *
            (
                (1 / ratioB2b1) ** (1/3) * (1 - (1 / ratio_tau)) +
                (1 / ratio_tau)
            ) ** (-3/7)
        )
        y2_gill_1981 = gill_1981 * y1

        lim_cheng_1998 = (1 / ratioB2b1) ** 0.75
        y2_lim_cheng_1998 = lim_cheng_1998 * y1

    live_bed_computed[study_key] = {
        "y2_Straub_1934": y2_straub_1934,
        "y2_Komura_1966": y2_komura_1966,
        "y2_Gill_1981": y2_gill_1981,
        "y2_Lim_Cheng_1998": y2_lim_cheng_1998,
    }

# Scour depth graphs live-bed
x_line = np.linspace(0, 0.5, 100)
y_line = x_line

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
markers = ['o', '+', 's', '^', 'x', 'D']
colors = ["#0072BD", "#D95319", "#EDB120", "#77AC30", "#7E2F8E", "#A2142F"]
labels = [
    'Straub (1934)', 'Ashida (1963)', 'Komura (1966)',
    'Gill (1981)', 'Rana (1986)', 'Nowroozpour and Ettema (2021)'
]
studies = [k.replace(" ", "_") for k in authors_live_bed]

# Straub (1934)
ax = axs[0, 0]
ax.plot(x_line, y_line, '-k', label='$Computed = Measured$')
for i, study in enumerate(studies):
    ax.plot(
        live_bed_measured_y2[study].values,
        live_bed_computed[study]["y2_Straub_1934"].values,
        marker=markers[i],
        linestyle='',
        color=colors[i],
        label=labels[i]
    )
ax.set_title("Equation (7) Straub (1934)")
ax.set_xlabel('Measured $y_{2}$ [m]')
ax.set_ylabel('Computed $y_{2}$ [m]')
ax.grid(True)

# Komura (1966)
ax = axs[0, 1]
ax.plot(x_line, y_line, '-k', label='$Computed = Measured$')
for i, study in enumerate(studies):
    ax.plot(
        live_bed_measured_y2[study].values,
        live_bed_computed[study]["y2_Komura_1966"].values,
        marker=markers[i],
        linestyle='',
        color=colors[i],
        label=labels[i]
    )
ax.set_title("Equation (10) Komura (1966)")
ax.set_xlabel('Measured $y_{2}$ [m]')
ax.set_ylabel('Computed $y_{2}$ [m]')
ax.grid(True)

# Gill (1981)
ax = axs[1, 0]
ax.plot(x_line, y_line, '-k', label='$Computed = Measured$')
for i, study in enumerate(studies):
    ax.plot(
        live_bed_measured_y2[study].values,
        live_bed_computed[study]["y2_Gill_1981"].values,
        marker=markers[i],
        linestyle='',
        color=colors[i],
        label=labels[i]
    )
ax.set_title("Equation (13) Gill (1981)")
ax.set_xlabel('Measured $y_{2}$ [m]')
ax.set_ylabel('Computed $y_{2}$ [m]')
ax.grid(True)

# Lim and Cheng (1998)
ax = axs[1, 1]
ax.plot(x_line, y_line, '-k', label='$Computed = Measured$')
for i, study in enumerate(studies):
    ax.plot(
        live_bed_measured_y2[study].values,
        live_bed_computed[study]["y2_Lim_Cheng_1998"].values,
        marker=markers[i],
        linestyle='',
        color=colors[i],
        label=labels[i]
    )
ax.set_title("Equation (15) Lim and Cheng (1998)")
ax.set_xlabel('Measured $y_{2}$ [m]')
ax.set_ylabel('Computed $y_{2}$ [m]')
ax.grid(True)

for ax in axs.flat:
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.autoscale(enable=False)  # Prevent autoscaling from changing limits

# Legend
handles, legend_labels = axs[1, 1].get_legend_handles_labels()
fig.legend(handles, legend_labels, loc='lower center', ncol=3)
plt.show()

# Save the figure
fig.savefig(
    r"..\Figures\Scour_depth_live_bed.png",
    dpi=300, bbox_inches='tight', pad_inches=0.1)
