import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

# loads the dataset xlsx file
file_path = os.path.join(os.path.dirname(__file__), 'Dataset.xlsx')
df = pd.read_excel(file_path)

#shows the basic info in the dataset
print("Dataset Shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

print("\nData Info:")
print(df.info())

print("\nBasic Statistics:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

# sorts the data by columns
print("\nCorrelation Matrix:")
print(df.corr(numeric_only=True))

#uses seaborn to help visualise
sns.set_style("whitegrid")

# titles the comparison 
print("\nComparing Abundance and Species Richness: Track vs Plume")

# Gets the F and p values i want for the species richness and the abundance
# row 2 is for abundance and 7 is for the sdpecies richness
# abundance
abundance_track_f = float(df.iloc[2, 3])  # Track F-value
abundance_track_p = float(df.iloc[2, 4])  # Track p-value
abundance_plume_f = float(df.iloc[2, 7])  # Plume F-value
abundance_plume_p = float(df.iloc[2, 8])  # Plume p-value
#species richness
richness_track_f = float(df.iloc[7, 3])  # Track F-value
richness_track_p = float(df.iloc[7, 4])  # Track p-value
richness_plume_f = float(df.iloc[7, 7])  # Plume F-value
richness_plume_p = float(df.iloc[7, 8])  # Plume p-value
#prints out the F and p values for abundance and richness in both the track and plume 
print(f"Abundance - Track: F = {abundance_track_f}, p = {abundance_track_p}")
print(f"Abundance - Plume: F = {abundance_plume_f}, p = {abundance_plume_p}")
print(f"Species Richness - Track: F = {richness_track_f}, p = {richness_track_p}")
print(f"Species Richness - Plume: F = {richness_plume_f}, p = {richness_plume_p}")

# makes a graph for comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

#Abundance comparison
metrics = ['Track', 'Plume']
abundance_f_values = [abundance_track_f, abundance_plume_f]
abundance_p_values = [abundance_track_p, abundance_plume_p]

# sorts out a visual display of the graph, using colour here lets me differentiate the bars it also adds a colour picker and edge colour selection through the imports
#this makes the graph look a lot neater, this section also sets the title of this graph, the label of the y axis and limits for thwe y axis
axes[0].bar(metrics, abundance_f_values, color=["#0095ff", "#ff7700"], edgecolor='black')
axes[0].set_ylabel('F-value', fontsize=12)
axes[0].set_title('ABUNDANCE - Site Effect Comparison', fontsize=12, fontweight='bold')
axes[0].set_ylim(0, max(abundance_f_values) * 1.2)
# the for loop here is to add F value and p value above each bar
for i, (f_val, p_val) in enumerate(zip(abundance_f_values, abundance_p_values)):
    axes[0].text(i, f_val + 0.5, f'F={f_val:.2f}\np={p_val:.6f}', ha='center', fontsize=10)
axes[0].grid(axis='y', alpha=0.3)

# Species richness comparison
richness_f_values = [richness_track_f, richness_plume_f]
richness_p_values = [richness_track_p, richness_plume_p]
# same as the abundance one but for richness
axes[1].bar(metrics, richness_f_values, color=["#00ff00", "#ff0000"], edgecolor='black')
axes[1].set_ylabel('F-value', fontsize=12)
axes[1].set_title('SPECIES RICHNESS - Site Effect Comparison', fontsize=12, fontweight='bold')
axes[1].set_ylim(0, max(richness_f_values) * 1.2)
for i, (f_val, p_val) in enumerate(zip(richness_f_values, richness_p_values)):
    axes[1].text(i, f_val + 0.5, f'F={f_val:.2f}\np={p_val:.6f}', ha='center', fontsize=10)
axes[1].grid(axis='y', alpha=0.3)
#makes the layout a bit nicer and shows the graph
plt.tight_layout()
plt.show()
#gives the results back in text as opposed to just a graph, saying significant if p < 0.05
print("\nInterpretation:")
print("Higher F-values indicate stronger differences between sites")
print("p-values < 0.05 indicate statistically significant differences")
print(f"Abundance: Track shows {'SIGNIFICANT' if abundance_track_p < 0.05 else 'NO'} difference (p={abundance_track_p:.6f})")
print(f"Abundance: Plume shows {'SIGNIFICANT' if abundance_plume_p < 0.05 else 'NO'} difference (p={abundance_plume_p:.6f})")
print(f"Species Richness: Track shows {'SIGNIFICANT' if richness_track_p < 0.05 else 'NO'} difference (p={richness_track_p:.6f})")
print(f"Species Richness: Plume shows {'SIGNIFICANT' if richness_plume_p < 0.05 else 'NO'} difference (p={richness_plume_p:.6f})")