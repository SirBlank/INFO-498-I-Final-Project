import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

files = {
    "As an AI Language Model": "C:\\Users\\magui\\Downloads\\as_an_ai_language_model_full.csv",
    "As of my Last Knowledge Update": "C:\\Users\\magui\\Downloads\\as_of_my_last_knowledge_update_full_missing_summary.csv",
    "Based on my Training Data": "C:\\Users\\magui\\Downloads\\based_on_my_training_data_full.csv",
    "For the Most Accurate and up-to-date Information": "C:\\Users\\magui\\Downloads\\for_the_most_accurate_and_up-to-date_information_full.csv",
    "I cannot Access real-time": "C:\\Users\\magui\\Downloads\\i_cannot_access_real-time_full.csv",
    "I don't have Access to real-time Data": "C:\\Users\\magui\\Downloads\\i_dont_have_access_to_real_time_data_full.csv",
    "My last Training cut-off": "C:\\Users\\magui\\Downloads\\my_last_training_cut-off_full.csv",
    "My Latest Knowledge Update": "C:\\Users\\magui\\Downloads\\my_latest_knowledge_update_full.csv"
}

dfs = []

for file_path in files.values():
    try:
        df1 = pd.read_csv(file_path, encoding='ISO-8859-1')
        dfs.append(df1)
    except UnicodeDecodeError:
        print(f"Error reading {file_path}. Please check the file encoding.")

df = pd.concat(dfs)

def add_percentages(ax, counts, total):
    for p in ax.patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        ax.annotate(percentage, (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

# Field of Study Bar Graph
field_of_study_counts = df['Field of Study'].value_counts().reindex(
    ['Arts', 'Humanities', 'Social Sciences', 'Natural Sciences', 'Applied Sciences'], fill_value=0)

plt.figure(figsize=(10, 6))
ax1 = field_of_study_counts.plot(kind='bar', color=['red', 'blue', 'green', 'orange', 'purple'])
plt.title('Fields of Study')
plt.xlabel('Field of Study')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
add_percentages(ax1, field_of_study_counts, field_of_study_counts.sum())
plt.show()

# Location of Key Phrase Bar Graph
location_counts = df[df['Location of Keyword'] != 'NA']['Location of Keyword'].str.lower().value_counts().reindex(
    ['abstract', 'introduction', 'methodology', 'literature review', 'result', 'discussion', 'conclusion'], fill_value=0)

plt.figure(figsize=(10, 6))
ax2 = location_counts.plot(kind='bar', color=['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink'])
plt.title('Where the Phrases are Found')
plt.xlabel('Location of Phrase')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
add_percentages(ax2, location_counts, location_counts.sum())
plt.show()

# Type of Article Pie Chart
type_of_article_counts = df['Type of Article'].value_counts().reindex(
    ['Book', 'Research'], fill_value=0)

plt.figure(figsize=(8, 8))
type_of_article_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Types of Medium for Articles')
plt.ylabel('')
plt.show()

# Removed or Not Pie Chart
removed_counts = df[df['Removed'] != 'NA']['Removed'].replace({'Y': 'Yes', 'N': 'No'}).value_counts().reindex(
    ['Yes', 'No'], fill_value=0)

plt.figure(figsize=(8, 8))
removed_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Removed Articles')
plt.ylabel('')
plt.show()

print("\nField of Study Counts:")
print(field_of_study_counts)

print("\nLocation of Keyword Counts:")
print(location_counts)

print("\nType of Article Counts:")
print(type_of_article_counts)

print("\nRemoved Counts:")
print(removed_counts)


summary_data = []


def process_file(phrase, file_path):
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print(f"Error reading {file_path}. Please check the file encoding.")
        return
    
    # Filter by year
    df_before_2022 = df[df['Year'] < 2022]
    df_2022_and_after = df[df['Year'] >= 2022]
    
    # Function to calculate metrics
    def calculate_metrics(df, label):
        total_publications = len(df)
        total_citations = df['Citation'].sum()
        average_publications_per_year = total_publications / len(df['Year'].unique()) if len(df['Year'].unique()) > 0 else 0
        average_citations_per_publication = total_citations / total_publications if total_publications != 0 else 0
        
        summary_data.append([phrase, label, total_publications, total_citations, average_publications_per_year, average_citations_per_publication])
    
    
    calculate_metrics(df_before_2022, "Before 2022")
    
    calculate_metrics(df_2022_and_after, "2022 and After")


for phrase, file_path in files.items():
    process_file(phrase, file_path)

# Create a summary DataFrame
summary_df = pd.DataFrame(summary_data, columns=['Phrase', 'Year Range', 'Total Publications', 'Total Citations', 'Average Publications per Year', 'Average Citations per Publication'])

summary_df = summary_df.round(2)

# Display the summary
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')
tbl = ax.table(cellText=summary_df.values, colLabels=summary_df.columns, cellLoc='center', loc='center')
tbl.auto_set_column_width(col=list(range(len(summary_df.columns))))
plt.title("Summary Data Table")
plt.show()

# Provided publication numbers
provided_publications = {
    2024: 1870000,
    2023: 7990000,
    2022: 5720000,
    2021: 4450000,
    2020: 4090000,
    2019: 3980000,
    2018: 3390000,
    2017: 5320000,
    2016: 5220000,
    2015: 5130000,
    2014: 5170000,
    2013: 5210000,
    2012: 5020000,
    2011: 4430000,
    2010: 4780000
}

# Calculate number of publications per year from combined data
publications_per_year = df['Year'].value_counts().sort_index()

# Create a DataFrame with the provided publication numbers
provided_df = pd.DataFrame(list(provided_publications.items()), columns=['Year', 'All Publications on Google Scholar'])

# Merge the calculated publications with the provided numbers
comparison_df = pd.DataFrame({'Year': publications_per_year.index, 'AI-Generated Publications on Google Scholar': publications_per_year.values})
comparison_df = comparison_df.round(2)
comparison_df = pd.merge(comparison_df, provided_df, on='Year', how='outer').fillna(0)
comparison_df = comparison_df.astype({'Year': 'int64', 'AI-Generated Publications on Google Scholar': 'int64', 'All Publications on Google Scholar': 'int64'})

# Filter to only include years 2010 to 2024
comparison_df = comparison_df.query('2010 <= Year <= 2024')

# Display the comparison DataFrame using matplotlib table
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('tight')
ax.axis('off')
tbl = ax.table(cellText=comparison_df.values, colLabels=comparison_df.columns, cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.2)
plt.title("Comparison of Publications Per Year")
plt.show()

combined_data = summary_df.groupby('Year Range').sum().reset_index()

# Plot the combined bar graph
fig, ax = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("All-Phrase Data", fontsize=16)

metrics = ['Total Publications', 'Total Citations', 'Average Publications per Year', 'Average Citations per Publication']
titles = ['Total Publications', 'Total Citations', 'Average Publications per Year', 'Average Citations per Publication']

for i, metric in enumerate(metrics):
    ax = plt.subplot(2, 2, i+1)
    bars = combined_data.plot(x='Year Range', y=metric, kind='bar', ax=ax, title=titles[i])
    ax.set_ylabel(metric)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.bar_label(bars.containers[0], label_type='center')


plt.tight_layout()
plt.show()