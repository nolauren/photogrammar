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

def get_page_w_id(link):
    """ Returns photo info (as soup obj) and photo id string """
    new_link = re.sub("/collection/fsa", "", link)
    photo_id = re.sub(loc_url_prefix, "", link)
    photo_id = re.sub("/PP/", "", photo_id)
    this_soup = load_page_as_soup(new_link)
    return photo_id, this_soup

def return_img_urls(soup_obj, photo_id):
    """ Turns mark webpage into a csv file and writes to disk """
    regex = re.compile('image/[a-z]+')
    urls = []
    for img in soup_obj.find_all('link', attrs={"rel": 'alternate', "type": regex}):
        urls.append(img.get("href"))
    return urls

def main():
    """ Downloads the marc records for urls in pickle/all_urls.p """
    with open(base_path + "pickle/all_urls.p", 'r') as f:
        all_links = pickle.load(f)
    error_links = []
    while all_links:
        for link in all_links:
            photo_id, this_soup = get_page_w_id(link)
            if this_soup != None:
                with open(base_path + "img_url/" + photo_id + ".txt", 'w')
                    these_urls = return_img_urls(this_soup, photo_id)
                    for url in these_urls: f.write(url + "\n")
                print("Done with photo " + photo_id)        
            else:
                error_links.append(link)
        all_links = error_links


if __name__ == "__main__":
    main()

