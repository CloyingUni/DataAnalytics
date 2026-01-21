import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

#loads the file
file_path = os.path.join(os.path.dirname(__file__), 'Dataset.xlsx')
df = pd.read_excel(file_path)

#this make sure it just gets the numbres from the dataset and not the words
df_numeric = df.iloc[:, 3:].apply(pd.to_numeric, errors='coerce')

print("\nDataset Info:")
print(f"Total rows: {len(df)}")
print(f"Numeric columns extracted: {df_numeric.shape[1]}")

# defines metrics and their rows
metrics_of_interest = [
    {'name': 'Abundance', 'row': 2},
    {'name': 'Species Richness', 'row': 7},
    {'name': 'Gini-Simpson Diversity', 'row': 12},
    {'name': "Simpson's Evenness", 'row': 17}
]
#creates a list that the resuklts can be put in
paired_results = []

print("\nPaired T-Tests:")

for metric in metrics_of_interest:
    row_idx = metric['row']
    name = metric['name']
    
    if row_idx < len(df):
        # gets F and p for track
        track_f = pd.to_numeric(df.iloc[row_idx, 3], errors='coerce')
        track_p = pd.to_numeric(df.iloc[row_idx, 4], errors='coerce')
        
        # does the same for plume
        plume_f = pd.to_numeric(df.iloc[row_idx, 7], errors='coerce')
        plume_p = pd.to_numeric(df.iloc[row_idx, 8], errors='coerce')
        
        # uses numpy to check nan values
        if not (np.isnan(track_f) or np.isnan(plume_f)):
            # finds the difference
            f_diff = track_f - plume_f
            p_diff = abs(track_p - plume_p)
            #adds results to the list that was made earlier
            paired_results.append({
                'Metric': name,
                'Track F': track_f,
                'Track p': track_p,
                'Plume F': plume_f,
                'Plume p': plume_p,
                'F Difference': f_diff,
                'Track Significant': 'Yes' if track_p < 0.05 else 'No',
                'Plume Significant': 'Yes' if plume_p < 0.05 else 'No'
            })
            # prints out results
            print(f"\n{name}:")
            print(f"  Track - F: {track_f:.4f}, p: {track_p:.6f} {'(SIGNIFICANT)' if track_p < 0.05 else ''}")
            print(f"  Plume - F: {plume_f:.4f}, p: {plume_p:.6f} {'(SIGNIFICANT)' if plume_p < 0.05 else ''}")
            print(f"  F Difference: {f_diff:.4f}")

if paired_results:
    #uses pandas to make the table of the results
    results_df = pd.DataFrame(paired_results)
    print("\nPaired t-test results in a table")
    print(results_df.to_string(index=False))
    
    # visualises the results for easier comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    metrics = [r['Metric'] for r in paired_results]
    track_f_vals = [r['Track F'] for r in paired_results]
    plume_f_vals = [r['Plume F'] for r in paired_results]
    track_p_vals = [r['Track p'] for r in paired_results]
    plume_p_vals = [r['Plume p'] for r in paired_results]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    # graph for the F comparison
    axes[0, 0].bar(x - width/2, track_f_vals, width, label='Track', color='#0095ff', edgecolor='black')
    axes[0, 0].bar(x + width/2, plume_f_vals, width, label='Plume', color='#ff7700', edgecolor='black')
    axes[0, 0].set_ylabel('F-value', fontsize=12)
    axes[0, 0].set_title('Track vs Plume - F-Values', fontsize=12, fontweight='bold')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels([m.replace(' ', '\n') for m in metrics], fontsize=9)
    axes[0, 0].legend()
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # graph for the p comparison
    axes[0, 1].bar(x - width/2, track_p_vals, width, label='Track', color='#00ff00', edgecolor='black')
    axes[0, 1].bar(x + width/2, plume_p_vals, width, label='Plume', color='#ff0000', edgecolor='black')
    axes[0, 1].axhline(y=0.05, color='black', linestyle='--', linewidth=2, label='α = 0.05')
    axes[0, 1].set_ylabel('P-value', fontsize=12)
    axes[0, 1].set_title('Track vs Plume - P-Values', fontsize=12, fontweight='bold')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels([m.replace(' ', '\n') for m in metrics], fontsize=9)
    axes[0, 1].legend()
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # graph for F differences
    f_diffs = [r['F Difference'] for r in paired_results]
    colors = ['#ff0000' if diff < 0 else '#0095ff' for diff in f_diffs]
    axes[1, 0].bar(metrics, f_diffs, color=colors, edgecolor='black')
    axes[1, 0].axhline(y=0, color='black', linestyle='-', linewidth=1)
    axes[1, 0].set_ylabel('F Difference (Track - Plume)', fontsize=12)
    axes[1, 0].set_title('F-Value Difference', fontsize=12, fontweight='bold')
    axes[1, 0].set_xticklabels([m.replace(' ', '\n') for m in metrics], fontsize=9)
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # graph for significance
    track_sig = [1 if r['Track Significant'] == 'Yes' else 0 for r in paired_results]
    plume_sig = [1 if r['Plume Significant'] == 'Yes' else 0 for r in paired_results]
    axes[1, 1].bar(x - width/2, track_sig, width, label='Track (p < 0.05)', color='#0095ff', edgecolor='black')
    axes[1, 1].bar(x + width/2, plume_sig, width, label='Plume (p < 0.05)', color='#ff7700', edgecolor='black')
    axes[1, 1].set_ylabel('Significant', fontsize=12)
    axes[1, 1].set_title('Statistical Significance', fontsize=12, fontweight='bold')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels([m.replace(' ', '\n') for m in metrics], fontsize=9)
    axes[1, 1].set_ylim([0, 1.2])
    axes[1, 1].legend()
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    #prints an explanation of the results
    print("Results:")
    print("- F-values show the strength of differences between sites")
    print("- P-values < 0.05 show statistically significant differences")
    print("- Red bars (F Difference) show plume has higher F-value")
    print("- Blue bars (F Difference) show track has higher F-value")

