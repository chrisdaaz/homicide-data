import requests
from bs4 import BeautifulSoup

def get_soup(base_url, page):
    """
    This returns a bunch of soup from a base url and a page. The page should
    be a string. This does not do any preprocessing to the soup

    ">>> get_soup("http://homicide.northwestern.edu/database/", "2")
    http://homicide.northwestern.edu/database/2
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

    <html>
    ..."

    """
    url = requests.compat.urljoin(base_url, page)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    print(url)
    return soup

def case_data(soup):
    # Check to see if the page is an actual database record
    if soup.find("h2"):
        case_desc = soup.find("h2").next_sibling.strip()
        # Get the keys
        keys = [x.text.strip() for x in soup.find_all('td', style="width: 200px; text-align:left; font-family: Arial Narrow,sans-serif; font-size: 12px;") if x.text]
        # Get the values
        values = [x.text.strip() for x in soup.find_all('td', style="width: 450px; text-align:left;") if x.text]
        # Pair the keys with the values
        data = dict(zip(keys, values))
        # Add case description to the case data
        data['case description'] = case_desc
        return data

def get_all_data(number_of_items):
    base_url = "http://homicide.northwestern.edu/database/"
    return [case_data(get_soup(base_url, str(item))) for item in range(1,number_of_items)]

# We used pandas to scrub the data and write to csv
