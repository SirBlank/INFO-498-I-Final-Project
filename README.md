# INFO-498-I Final Project

This is the technical component of our INFO 498-I final project.

## web-scraping.py
**web-scraping.py** is a Python script that enables you to scrape Google Scholar URLs for information such as publication titles, publishers, publication dates, and more.

### Getting Started
1. Clone this repository to your local machine.
2. On Google Scholar, enter your search query and apply any desired filters. Copy the search URL as shown below.
   ![Google Scholar Search](https://github.com/SirBlank/INFO-498-I-Final-Project/assets/114832146/c53fb48e-556e-4b7c-b61b-d6e8cea21e1c)
3. Paste the URL in the specified location in **web-scraping.py**. Follow the example URL format. Add 'start={i}&' to scrape all search results. Adjust 'i' to specify the number of search results you wish to scrape.
   ![URL Example](https://github.com/SirBlank/INFO-498-I-Final-Project/assets/114832146/c0752260-1834-4b2a-8b86-541ce5116ff8)
4. Run the script!

**Note:** The script may take a long time to complete depending on the number of search results you want to scrape, so please be patient.

**Another Note:** The script might not run consistently if you attempt to scrape more than 200 articles in a single run, as Google tends to block queries with a large number of requests. If you need to scrape more than 200 articles, run the script multiple times with different 'i' values each time.

## data
The **data** folder contains all the cleaned data we have scraped and used for analysis in this project.

### Column Descriptions

| Column Name          | Description                                                                                                        |
|----------------------|--------------------------------------------------------------------------------------------------------------------|
| Paper Title          | Title of the article                                                                                               |
| Year                 | Year of publication                                                                                                |
| Author               | Author of publication                                                                                              |
| Citation             | Number of times other publications have cited this article                                                         |
| Url of paper         | URL of the paper                                                                                                   |
| Summary              | Snippet of text that contained the formatted ChatGPT response                                                      |
| Field of Study       | The academic field to which the paper belongs (Arts, Humanities, Social Sciences, Natural Sciences, Applied Sciences) |
| Location of Keyword  | Section of the paper where the keyword is found (Abstract, Introduction, Literature Review, Methodology, Result, Discussion, Conclusion)  |
| Type of Article      | The type of publication (Book, Research)                                                                           |
| Removed              | Whether the keyword has been removed from the most recent version of the article (Y for Yes, N for No)             |
| Notes                | Any interesting observations made while manually labeling these data                                               |

## data_analytics.py and data_analytics2.py
These scripts contain the data analysis and visualizations used to generate the visualizations in our final report.
