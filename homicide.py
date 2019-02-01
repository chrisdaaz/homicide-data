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

    """ takes soup and returns a dictionary. The dictionary is namespaced using
    a highly opinionated idea: if there's an key or value, look above and run
    TODO: Add a doc test if necessary.
    """
    # Check to see if the page is an actual database record
    key_search ="width: 200px; text-align:left; font-family: Arial Narrow,sans-serif; font-size: 12px;"
    value_search = "width: 450px; text-align:left;"
    if soup.find("h2"):
        case_desc = soup.find("h2").next_sibling.strip()
        # Get the values for keys, namespace them by the previous H2 so that we don't end up with two of the same fields
        keys = [ "{}-{}".format(k.find_previous('h2').text.strip(), k.text.strip()).lower().title().replace("'", "")
                for k in soup.find_all('td', style=key_search)
                if k.text]
        # get the values
        values = [v.text.strip() for v in soup.find_all('td', style=value_search) if v.text]
        # create a list of Dictionaries
        data = dict(zip(keys, values))
        # Add case description to the case data
        data['CaseDescription'] = case_desc
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
def write_md(data, directory):
    import os
    for item in data:

        filename = "{}.md".format(item["CaseDescriptionCaseNumber"])
        with open(os.path.join(directory, filename), 'w') as f:
            f.write("--- \n")
            for key, value in item.items():
                f.write("{}: {}\n".format(key, value))
            f.write("---")

"""
OR

            for key, value in item.items():
                f.write("{}: "{}"\n".format(key, value))
            f.write("\n---")

if the above doesn't work:
    Ah. There's also something called Yaml pipe style that might do it:
    key: | This is my "goofy" 'string'
"""

def main(number_of_items, csv_file, output_dir_for_md):

    """
    This goes through a range of items in the homicide database and outputs markdown files with yaml frontmatter
    as well as a csv data file

    Takes three arguments:

    number_of_items --> number of data pages you want to process from homicide
    csv_file --> the output of the csv data file
    output_dir_for_md --> the output directory for the .md files
    """
    data = [d for d in get_all_data(number_of_items) if d]
    write_md(data, output_dir_for_md)
    df = pandas.DataFrame.from_dict(data)
    df.to_csv(csv_file, index=False)
