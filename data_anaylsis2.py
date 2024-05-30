import pandas as pd
import matplotlib.pyplot as plt

file1 = 'C:/Users/magui/Downloads/my_last_training_cut-off_full.csv'
file2 = 'C:/Users/magui/Downloads/as_of_my_last_knowledge_update_full_missing_summary.csv'
file3 = 'C:/Users/magui/Downloads/i_dont_have_access_to_real_time_data_full.csv'

df1 = pd.read_csv(file1, encoding='ISO-8859-1')
df2 = pd.read_csv(file2, encoding='ISO-8859-1')
df3 = pd.read_csv(file3, encoding='ISO-8859-1')
df = pd.concat([df1, df2, df3])

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
