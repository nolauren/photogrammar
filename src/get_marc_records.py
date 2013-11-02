import urllib
import pickle
import re

from bs4 import BeautifulSoup

base_path = "/Users/tba3/Desktop/files/fsa_rescrape/"
loc_url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"

def load_page_as_soup(page_url):
    """ Loads url in a soup obj; returns None if not succesful """
    try:
        f = urllib.urlopen(page_url)
        s = f.read()
        f.close()
        soup = BeautifulSoup(s)
        return soup
    except IOError:
        return None
    except:
        return None

def get_marc_w_id(link):
    """ Returns mark records (as soup obj) and photo id string """
    new_link = re.sub("/collection/fsa", "", link) + "marc/"
    photo_id = re.sub(loc_url_prefix, "", link)
    photo_id = re.sub("/PP/", "", photo_id)
    this_soup = load_page_as_soup(new_link)
    return photo_id, this_soup

def save_marc_record(soup_obj, photo_id):
    """ Turns mark webpage into a csv file and writes to disk """
    path_prefix = base_path + "marc_records/"
    with open(path_prefix + photo_id + ".csv", 'w') as f:
        for link in soup_obj.find_all('tr'):
            row_text = []
            for row in link.find_all('td'):
                row_text.append(re.sub(u',', u'', row.get_text()))
            if len(row_text) == 5:
                f.write(u','.join(row_text).encode('utf-8'))
                f.write('\n')

def main():
    """ Downloads the marc records for urls in pickle/all_urls.p """
    with open(base_path + "pickle/all_urls.p", 'r') as f:
        all_links = pickle.load(f)
    error_links = []
    while all_links:
        for link in all_links:
            photo_id, this_soup = get_marc_w_id(link)
            if this_soup != None:
                save_marc_record(this_soup, photo_id)
                print("Done with link " + photo_id)        
            else:
                error_links.append(link)
        all_links = error_links

if __name__ == "__main__":
    main()



