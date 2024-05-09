import pandas as pd
import matplotlib.pyplot as plt

csv_all_time = 'C:/Users/magui/Downloads/as_of_my_last_knowledge_update_full_missing_summary.csv'
csv_before_2022 = 'C:/Users/magui/Downloads/as_of_my_last_knowledge_update_before_2022.csv'
csv_after_2022 = 'C:/Users/magui/Downloads/as_of_my_last_knowledge_update_after_2022.csv'

# Convert to dataframes
df_all_time = pd.read_csv(csv_all_time)
df_before_2022 = pd.read_csv(csv_before_2022)
df_after_2022 = pd.read_csv(csv_after_2022)

# Function to calculate metrics
def calculate_metrics(df):
    total_papers = len(df)
    total_citations = df['Citation'].fillna(0).astype(int).sum()
    avg_citations = total_citations / total_papers if total_papers != 0 else 0
    return total_papers, total_citations, round(avg_citations, 2)

metrics_all_time = calculate_metrics(df_all_time)
metrics_before_2022 = calculate_metrics(df_before_2022)
metrics_after_2022 = calculate_metrics(df_after_2022)

# Create a DataFrame
summary_df = pd.DataFrame({
    'Timeframe': ['Before 2022', 'After 2022', 'All Time'],
    'Total Publications': [metrics_before_2022[0], metrics_after_2022[0], metrics_all_time[0]],
    'Total Citations': [metrics_before_2022[1], metrics_after_2022[1], metrics_all_time[1]],
    'Average Citations per Publication': [metrics_before_2022[2], metrics_after_2022[2], metrics_all_time[2]]
})

colors = ['blue', 'green', 'orange']

# Plot the results with a title
fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# Plot total publications
ax[0].bar(summary_df['Timeframe'], summary_df['Total Publications'], color=colors[0])
ax[0].set_title('Total Publications')
ax[0].set_ylabel('Number of Publications')

# Plot total citations
ax[1].bar(summary_df['Timeframe'], summary_df['Total Citations'], color=colors[1])
ax[1].set_title('Total Citations')
ax[1].set_ylabel('Number of Citations')

# Plot average citations
ax[2].bar(summary_df['Timeframe'], summary_df['Average Citations per Publication'], color=colors[2])
ax[2].set_title('Average Citations per Publication')
ax[2].set_ylabel('Average Citations')

fig.suptitle('"As of My Last Knowledge Update" Data from Google Scholar', fontsize=16)

# Table Creation
fig, ax_table = plt.subplots(figsize=(10, 4))
ax_table.axis('off')
table = ax_table.table(cellText=summary_df.values, colLabels=summary_df.columns, cellLoc='center', loc='center')
table.set_fontsize(14) 
table.scale(1.2, 1.2)

plt.tight_layout()
plt.show()