import requests
from bs4 import BeautifulSoup
import pandas

def get_soup(base_url, page):
    """
    This scrapes HTML from a base url and a page reference. The page should
    be a string. This does not do any preprocessing to the HTML.

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

def format_key(key):
    """this formats soup into a unique key"""
    return "{} {}".format(key.find_previous('h2').text.strip(), key.text.strip()).title().replace("'", "").replace(" ", "").replace("?", "")

def case_data(soup):

    """
    This takes the scraped HTML and returns a dictionary. The dictionary is namespaced using
    a highly opinionated idea: if there's a key or a value, look above and grab the heading and append it to the beginning of the key using titlecase (e.g. DefendantName).
    """
    key_search ="width: 200px; text-align:left; font-family: Arial Narrow,sans-serif; font-size: 12px;"
    # Check to see if the page is an actual database record
    if soup.find("h2"):
        # If so, grab the case CaseDescription
        case_desc = soup.find("h2").next_sibling.strip()
        # Next, get the values for keys and namespace them to prevent duplicates
        keys_and_values = [(format_key(k), k.find_next('td').text.strip()) for k in soup.find_all('td', style=key_search) if k.text]
        # create a list of Dictionaries
        data = dict(keys_and_values)
        # Add case description to the case data
        data['CaseDescription'] = case_desc
        return data
    else:       
        print("Not a database record")

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

def write_md(data, directory):
    import os
    for item in data:
        filename = "{}.md".format(item["CaseDescriptionCaseNumber"])
        with open(os.path.join(directory, filename), 'w') as f:
            f.write("--- \n")
            for key, value in item.items():
                f.write("{}: {}\n".format(key, value))
            f.write("---")

def main(number_of_items, csv_file, output_dir_for_md):

    """
    This goes through a range of items in the homicide database and outputs markdown files with yaml frontmatter
    as well as a csv data file

    Takes three arguments:

    number_of_items --> number of data pages you want to process from homicide
    csv_file --> the output of the csv data file
    output_dir_for_md --> the output directory for the .md files

    Example:
    >>> homicide.main(200, "/home/nulibrec/homicide/homicide-20190205.csv", "/home/nulibrec/homicide/homicide-md/")

    Or shh:
    >>> /home/nulibrec/homicide
    """
    data = [d for d in get_all_data(number_of_items) if d]
    write_md(data, output_dir_for_md)
    df = pandas.DataFrame.from_dict(data)
    # Start the index at 1
    df.index = df.index + 1
    df.to_csv(csv_file, index=True, index_label="IndexId")
