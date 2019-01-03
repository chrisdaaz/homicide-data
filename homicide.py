import requests
import csv
from bs4 import BeautifulSoup

def get_soup(url, page):
    url = requests.compat.urljoin(url, str(page))
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    print(url)
    return soup

def case_data(soup):
    """
    grabs case-specific table data, returns as a comma-separated list
    >>> [x.
    text.strip() for x in soup.find_all('td', style="width: 450px; text-align:left;")]
    """

    #get case description
    if soup.find("h2"):
        case_desc = soup.find("h2").next_sibling.strip()
        #get the keys

        keys = [x.text.strip() for x in soup.find_all('td', style="width: 200px; text-align:left; font-family: Arial Narrow,sans-serif; font-size: 12px;") if x.text]
        # get the values
        values = [x.text.strip() for x in soup.find_all('td', style="width: 450px; text-align:left;") if x.text]
        data = dict(zip(keys, values))
        data['case description'] = case_desc
        return data

def get_all_data(number_of_items):
    base_url = "http://homicide.northwestern.edu/database/"
    return [case_data(get_soup(base_url, item)) for item in range(1,number_of_items)]

def save_csv():
    with open('homicide_db.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(case_record)
