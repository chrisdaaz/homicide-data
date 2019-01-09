import requests
from bs4 import BeautifulSoup
import pandas

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
        # create a list of lists
        data = list(zip(keys, values))
        # Add case description to the case data
        data.append(('case description', case_desc))
        return data

def get_all_data(number_of_items):
    """
    Enter in a number for the top range of the iteration (i.e. >11020).
    >>> get_all_data(10)
        http://homicide.northwestern.edu/database/1
        http://homicide.northwestern.edu/database/2
        http://homicide.northwestern.edu/database/3
        http://homicide.northwestern.edu/database/4
        http://homicide.northwestern.edu/database/5
        http://homicide.northwestern.edu/database/6
        http://homicide.northwestern.edu/database/7
        http://homicide.northwestern.edu/database/8
        http://homicide.northwestern.edu/database/9
        ...
    """
    base_url = "http://homicide.northwestern.edu/database/"
    return [case_data(get_soup(base_url, str(item))) for item in range(1,number_of_items)]

def main(number_of_items, csv_file):
    data = [d for d in get_all_data(number_of_items) if d]
    # TODO: make a blank dataframe , for item in data make a dataframe, then merge it with the previous dataframe
    df = pandas.DataFrame(data)
    df.to_csv(csv_file, index=False)

"""
from slack:

I think I found it... https://stackoverflow.com/questions/44280227/zip-two-lists-in-dictionary-but-keep-duplicates-in-key
Stack Overflow
Zip two lists in dictionary but keep duplicates in key
I have two lists: alist = ['key1','key2','key3','key3','key4','key4','key5'] blist= [30001,30002,30003,30003,30004,30004,30005] I want to merge these lists and add them to a dictionary. I try ...

I wonder if pandas can cope with defaultdict
```>>> from collections import defaultdict

>>> my_dict = defaultdict(list)
>>> for k, v in zip(alist, blist):
...     my_dict[k].append(v)
...
>>> my_dict
defaultdict(<type 'list'>, {'key3': [30003, 30003], 'key2': [30002], 'key1': [30001], 'key5': [30005], 'key4': [30004, 30004]})```
(edited)
The problem is i can't visualize how pandas will deal with the duplicates. Is there only a couple that are duped like "Name" ? maybe it's best to just deal with those two?
I'm back to thinking about namespacing based on the headers

david.schober [4:35 PM]
Figured it out! We can just use a ‘find_previous(h2)@
"""
