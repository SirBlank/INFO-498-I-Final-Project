import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
import random

# Scrapes publications queried through Google Scholar.

# Defining user agents
user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

# Rotating user agents for each query
for _ in user_agent_list:
  user_agent = random.choice(user_agent_list)
  headers = {'User-Agent': user_agent}

# Extracting html from query url
def get_paperinfo(paper_url):
    response = requests.get(paper_url, headers=headers)
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')
    paper_doc = BeautifulSoup(response.text, 'html.parser')
    return paper_doc

# Parsing through html for relevant paper information like number of citations, url, and author.
def get_tags(doc):
    paper_tag = doc.select('[data-lid]')
    cite_tag = doc.find_all('a', href=lambda href: '/scholar?cites=' in href)
    link_tag = doc.find_all('h3', {"class" : "gs_rt"})
    author_tag = doc.find_all("div", {"class": "gs_a"})
    summary_tag = doc.find_all('div', {"class": "gs_rs"})
    return paper_tag, cite_tag, link_tag, author_tag, summary_tag

# Extracting paper title
def get_papertitle(paper_tag):
    paper_names = [tag.select_one('h3').get_text() for tag in paper_tag if tag.select_one('h3')]
    return paper_names

# Extracting number of times other publications cited this paper.
def get_citecount(paper_tag):
    cite_counts = []
    for tag in paper_tag:
        cite_tag = tag.find('a', href=lambda href: '/scholar?cites=' in href)
        if cite_tag:
            cite_count = int(re.search(r'\d+', cite_tag.text).group()) if re.search(r'\d+', cite_tag.text) else 0
        else:
            cite_count = 0
        cite_counts.append(cite_count)
    return cite_counts

# Extracting paper url.
def get_link(link_tag):
    links = [link_tag.a['href'] for link_tag in link_tag if link_tag.a]
    return links

# Extracting author, publication year, and publisher
def get_author_year_publi_info(authors_tag):
    years = [int(re.search(r'\d+', tag.text).group()) for tag in authors_tag if re.search(r'\d+', tag.text)]
    publication = [tag.text.split()[-1] for tag in authors_tag]
    authors = [tag.text.split()[0] + ' ' + re.sub(',', '', tag.text.split()[1]) for tag in authors_tag]
    return years, publication, authors

# Extracting snippet of text that contained the keywords from the query.
def get_summary(summary_tag):
    summaries = [tag.get_text(strip=True) for tag in summary_tag]
    return summaries

paper_repos_dict = {
    'Paper Title': [],
    'Year': [],
    'Author': [],
    'Citation': [],
    'Publication': [],
    'Url of paper': []
}

# Compiling all paper information into a single dataframe.
def add_in_paper_repo(papername, year, author, cite, publi, link, summary):
    max_len = max(len(papername), len(year), len(author), len(cite), len(publi), len(link), len(summary))
    
    papername.extend([None]*(max_len - len(papername)))
    year.extend([None]*(max_len - len(year)))
    author.extend([None]*(max_len - len(author)))
    cite.extend([0]*(max_len - len(cite)))
    publi.extend([None]*(max_len - len(publi)))
    link.extend([None]*(max_len - len(link)))
    summary.extend([None]*(max_len - len(summary)))
    
    paper_repos_dict['Paper Title'] = papername
    paper_repos_dict['Year'] = year
    paper_repos_dict['Author'] = author
    paper_repos_dict['Citation'] = cite
    paper_repos_dict['Publication'] = publi
    paper_repos_dict['Url of paper'] = link
    paper_repos_dict['Summary'] = summary
    
    return pd.DataFrame(paper_repos_dict)


all_dataframes = []
i = 0

while True:
    # CHANGE QUERY URL HERE
    url = f"https://scholar.google.com/scholar?start={i}&hl=en&as_sdt=0%2C48&q=%22My+last+training+cut+off%22+-GPT+-ChatGPT&btnG="
    # EXAMPLE:
    # url = f"https://scholar.google.com/scholar?start={i}&hl=en&as_sdt=0%2C48&q=%22As+of+my+last+knowledge+update%22+-%22ChatGPT%22&oq="
    doc = get_paperinfo(url)
    paper_tag, cite_tag, link_tag, author_tag, summary_tag = get_tags(doc)
    if not paper_tag:
        break
    paper_tag, cite_tag, link_tag, author_tag, summary_tag = get_tags(doc)
    papername = get_papertitle(paper_tag)
    year, publication, author = get_author_year_publi_info(author_tag)
    cite = get_citecount(paper_tag)
    link = get_link(link_tag)
    summary = get_summary(summary_tag)
    final = add_in_paper_repo(papername, year, author, cite, publication, link, summary)

    all_dataframes.append(final)
    i += 10
    sleep_time = random.uniform(5, 30)
    sleep(sleep_time)

# Returning a csv file containing all scraped data
result_df = pd.concat(all_dataframes, ignore_index=True)
result_df.to_csv('my_last_training_cut_off_full.csv', index=False, encoding='utf-8')

print(final)
