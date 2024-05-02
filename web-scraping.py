from bs4 import BeautifulSoup
import requests
import csv

# frequently change user-agent or add a proxy
# figure out how to parse through multiple pages

# Define what application, os, vendor, basically the specs of the end-user, that is used to access web browsers.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
}

# Define google scholar query
url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C48&q=%22As+of+my+last+knowledge+update%22+-%22GPT%22&oq='

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'lxml')

# Create a CSV file
with open('google_scholar_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(['Title', 'Link', 'Summary'])

    # Iterate through each item in the soup
    for item in soup.select('[data-lid]'):
        try:
            print('---------------------------------------------')
            title = item.select('h3')[0].get_text(strip=True)
            print(title)
            link = item.select('a')[0]['href']
            print(link)
            summary = item.select('.gs_rs')[0].get_text(strip=True)
            print(summary)
            
            # Write the data to the CSV file
            writer.writerow([title, link, summary])
            
        except Exception as e:
            print(e)
