import urllib2
import pickle
import re

from bs4 import BeautifulSoup

verbose = TRUE
testing = TRUE
base_path = "/Users/tba3/Desktop/files/photogrammar/"
loc_url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"

def load_page_as_soup(page_url):
    """ Loads url in a soup obj; returns None if not succesful """
    try:
        f = urllib2.urlopen(page_url, timeout=5)
        s = f.read()
        f.close()
        soup = BeautifulSoup(s)
        return soup
    except IOError:
        return None
    except:
        return None

def get_this_page_links(soup_obj):
    """ Takes a soup object and extracts photo page urls  """
    output = []
    for link in soup_obj.find_all('a', attrs={"class": None}):
        this_link = link.get('href', default="")
        if re.match(loc_url_prefix, this_link): 
            output.append(this_link)
    return output

def get_these_pages_links(page_ids):
    """ Takes indicies, any subset of range(8766), and extracts urls from them """
    url_prefix = "http://www.loc.gov/pictures/search/?sp="
    url_suffix = "&co=fsa"
    all_links = []
    page_errors = []
    for index in page_ids: 
        url_name = url_prefix + str(index)+ url_suffix
        this_soup = load_page_as_soup(url_name)
        if this_soup == None:
            page_errors.append(index)
        else:
            these_links = get_this_page_links(this_soup)
            all_links += these_links
            if verbose: print("Done with page " + str(index))
    return all_links, page_errors

def main():
    """ Scrapes LOC website to get all photo ids """
    if testing:
        page_ids = [50,51]
    else:
        page_ids = range(8766)
    while page_ids:
        all_links, page_errors = get_these_pages_links(page_ids)
        page_ids = page_errors
    with open(base_path + "pickle/all_urls.p", 'w') as f:
        pickle.dump(all_links, f)

if __name__ == "__main__":
    main()













