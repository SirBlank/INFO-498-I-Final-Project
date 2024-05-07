import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

def get_paperinfo(paper_url):
    response = requests.get(paper_url, headers=headers)
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')
    paper_doc = BeautifulSoup(response.text, 'html.parser')
    return paper_doc

def get_tags(doc):
    paper_tag = doc.select('[data-lid]')
    cite_tag = doc.find_all('a', href=lambda href: '/scholar?cites=' in href)
    link_tag = doc.find_all('h3', {"class" : "gs_rt"})
    author_tag = doc.find_all("div", {"class": "gs_a"})
    return paper_tag, cite_tag, link_tag, author_tag

def get_papertitle(paper_tag):
    paper_names = [tag.select_one('h3').get_text() for tag in paper_tag if tag.select_one('h3')]
    return paper_names

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

def get_link(link_tag):
    links = [link_tag.a['href'] for link_tag in link_tag if link_tag.a]
    return links

def get_author_year_publi_info(authors_tag):
    years = [int(re.search(r'\d+', tag.text).group()) for tag in authors_tag if re.search(r'\d+', tag.text)]
    publication = [tag.text.split()[-1] for tag in authors_tag]
    authors = [tag.text.split()[0] + ' ' + re.sub(',', '', tag.text.split()[1]) for tag in authors_tag]
    return years, publication, authors

paper_repos_dict = {
    'Paper Title': [],
    'Year': [],
    'Author': [],
    'Citation': [],
    'Publication': [],
    'Url of paper': []
}

def add_in_paper_repo(papername, year, author, cite, publi, link):
    max_len = max(len(papername), len(year), len(author), len(cite), len(publi), len(link))
    
    papername.extend([None]*(max_len - len(papername)))
    year.extend([None]*(max_len - len(year)))
    author.extend([None]*(max_len - len(author)))
    cite.extend([0]*(max_len - len(cite)))
    publi.extend([None]*(max_len - len(publi)))
    link.extend([None]*(max_len - len(link)))
    
    paper_repos_dict['Paper Title'] = papername
    paper_repos_dict['Year'] = year
    paper_repos_dict['Author'] = author
    paper_repos_dict['Citation'] = cite
    paper_repos_dict['Publication'] = publi
    paper_repos_dict['Url of paper'] = link
    
    return pd.DataFrame(paper_repos_dict)

all_dataframes = []
i = 0

while True:  
    url = f"https://scholar.google.com/scholar?start={i}&hl=en&as_sdt=0%2C48&q=%22As+of+my+last+knowledge+update%22+-%22ChatGPT%22&oq="
    doc = get_paperinfo(url)
    paper_tag, _, _, _ = get_tags(doc)
    if not paper_tag:
        break
    paper_tag, cite_tag, link_tag, author_tag = get_tags(doc)
    papername = get_papertitle(paper_tag)
    year, publication, author = get_author_year_publi_info(author_tag)
    cite = get_citecount(paper_tag)
    link = get_link(link_tag)
    final = add_in_paper_repo(papername, year, author, cite, publication, link)
    all_dataframes.append(final)
    i += 10
    sleep(30)

result_df = pd.concat(all_dataframes, ignore_index=True)
result_df.to_csv('google_scholar_results.csv', index=False, encoding='utf-8')

print(final)
