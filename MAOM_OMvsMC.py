import sys
print(sys.executable)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("/Users/dantecangemi/Python Projects/Coastal Change Lab/MAOM/MAOM_plots/MAOM OM vs BD and MC(Sheet1).csv")

print("DATA LOADED")
print(df.head())

# ----------------------------
# CLEAN COLUMN NAMES
# ----------------------------
df.columns = df.columns.str.strip()

# ----------------------------
# FORCE NUMERIC
# ----------------------------
df["Organic Matter Content (%)"] = pd.to_numeric(df["Organic Matter Content (%)"], errors="coerce")
df["Moisture Content (%)"] = pd.to_numeric(df["Moisture Content (%)"], errors="coerce")

# Remove bad rows
clean_df = df.dropna(subset=["Organic Matter Content (%)", "Moisture Content (%)"])

# ----------------------------
# GROUPING
# ----------------------------
clean_df["group"] = clean_df["Sample ID"].str[:2]

# ----------------------------
# CUSTOM COLOR MAP (EDIT THIS)
# ----------------------------
palette = {
    "AP": "red",
    "FC": "blue",
    "LN": "green",
    "CM": "purple",
    "WR": "orange",
    "FP": "brown",
    "SI": "pink"
}

# ----------------------------
# VARIABLES
# ----------------------------
x = clean_df["Organic Matter Content (%)"].values
y = clean_df["Moisture Content (%)"].values

# ----------------------------
# REGRESSION
# ----------------------------
slope, intercept = np.polyfit(x, y, 1)
y_pred = slope * x + intercept

# ----------------------------
# R²
# ----------------------------
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r2 = 1 - (ss_res / ss_tot)

# ----------------------------
# PLOT
# ----------------------------
sns.set(style="whitegrid")
plt.figure(figsize=(8,6))

ax = sns.scatterplot(
    data=clean_df,
    x="Organic Matter Content (%)",
    y="Moisture Content (%)",
    hue="group",
    palette=palette
)

# ----------------------------
# TRENDLINE (ALL DATA)
# ----------------------------
x_line = np.linspace(min(x), max(x), 100)
y_line = slope * x_line + intercept

plt.plot(x_line, y_line, color="black", linewidth=2, label="Trendline (All Data)")

# ----------------------------
# LABEL POINTS
# ----------------------------
for i in clean_df.index:
    plt.text(
        clean_df.loc[i, "Organic Matter Content (%)"],
        clean_df.loc[i, "Moisture Content (%)"],
        clean_df.loc[i, "Sample ID"],
        fontsize=8,
        alpha=0.8,
        ha="right",
        va="bottom"
    )

# ----------------------------
# R² DISPLAY
# ----------------------------
plt.text(
    0.05,
    0.95,
    f"R² = {r2:.3f}",
    transform=plt.gca().transAxes,
    fontsize=12,
    verticalalignment='top'
)

# ----------------------------
# FORMATTING
# ----------------------------
plt.xlabel("Organic Matter Content (%)")
plt.ylabel("Moisture Content (%)")
plt.title("Organic Matter vs Moisture Content by Site Group")

plt.legend(title="Group")
plt.tight_layout()


plt.savefig(
    "/Users/dantecangemi/Python Projects/Coastal Change Lab/MAOM/MAOM_plots/MAOM_OMvsMC_plot.pdf",
    dpi=600,
    bbox_inches="tight"
)

plt.show()