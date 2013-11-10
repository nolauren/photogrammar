#!/usr/bin/env python
""" Downloads the location of the images hosted on the loc site

Using the photo ids obtained in script01, this downloads and parses
all of the main image information pages and extracts the location of
the stored images.
"""

import os
import urllib
import re
import socket
import copy

from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup

# Global variables
TESTING_FLAG = False
BASE_PATH = "/Users/tba3/Desktop/files/photogrammar/"

# Meta data
__author__ = "Taylor B. Arnold"
__date__ = "3 November 2013"
__contact__ = "taylor.b.arnold <at> gmail.com"
__version__ = "0.1.3"

def get_all_links():
    """ Reads files in photo_ids; returns every available url """
    current_id_files = os.listdir(BASE_PATH + "photo_ids")
    current_id_files = [BASE_PATH + "photo_ids/" + x for x in current_id_files]
    all_links = []
    for file in current_id_files:
        with open(file, 'r') as f:
            x = f.read()
            all_links += x.split("\n")[:20]
    return all_links

def download_info_html(this_url):
    """ Downloads a local copy of this_url """
    url_prefix = "http://www.loc.gov/pictures/item/"
    url_suffix = "/PP/"
    save_to = re.sub(url_prefix, "", this_url)
    save_to = re.sub(url_suffix, "", save_to)
    save_to = re.sub("/", "", save_to)
    save_to = BASE_PATH + "html/info/" + save_to + ".html"
    try:
        if not os.path.exists(save_to):
            urllib.urlretrieve(this_url, save_to)
        else: 
            pass
    except IOError:
        pass
    except:
        pass

def return_img_urls(soup_obj, photo_id):
    """ Turns mark webpage into a csv file and writes to disk """
    regex = re.compile('image/[a-z]+')
    urls = []
    for img in soup_obj.find_all('link', attrs={"rel": 'alternate', "type": regex}):
        urls.append(img.get("href"))
    return urls

def get_info_w_id(link):
    """ Returns info records (as soup obj) and photo id string """
    loc_url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"
    new_link = re.sub("/collection/fsa", "", link)
    download_info_html(new_link)
    return 0

def save_info_record(this_file):
    """ Turns mark webpage into a csv file and writes to disk """
    path_prefix = BASE_PATH + "marc_records/"
    file_out = path_prefix + re.sub("\.html", ".csv", this_file)
    if not os.path.exists(file_out):
        with open(BASE_PATH + "html/marc/" + this_file) as g:
            s = g.read()
            soup_obj = BeautifulSoup(s)
        with open(file_out, 'w') as f:
            for link in soup_obj.find_all('tr'):
                row_text = []
                for row in link.find_all('td'):
                    row_text.append(re.sub(u',', u'', row.get_text()))
                if len(row_text) == 5:
                    f.write(u','.join(row_text).encode('utf-8'))
                    f.write('\n')

def check_records(all_links):
    """ Checks that there exists a marc record csv for every file """
    finished_marc_records = os.listdir(BASE_PATH + "marc_records")
    all_links_names = []
    url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"
    url_suffix = "/PP"
    for link in all_links:
        regex = re.compile("("+url_prefix+")|("+url_suffix+")|(/info/)|(/)") 
        link = re.sub(regex, "", link)
        all_links_names.append(link + ".csv")
    set_diff = list(set(all_links_names) - set(finished_marc_records))
    set_diff = [re.sub("\.csv", "", x) for x in set_diff]
    set_diff = [url_prefix + x + url_suffix + "/" for x in set_diff] 
    return set_diff

def process_these_marc_urls(links):
    """ Process all urls in 'links' """
    these_links = copy.copy(links)
    while these_links:
        # Download a local copy of the photo info files
        pool = ThreadPool(processes=10)
        result = pool.map(get_info_w_id, these_links)
        pool.close()
        del pool

        # Parse marc html files; save as csv
        marc_files = os.listdir(BASE_PATH + "/html/marc")
        for this_file in marc_files:
            save_marc_record(this_file)

        # Check if all records in all_links are parsed
        these_links = check_records(links)

def main():
    """ Run all marc records or a test set """
    all_links = get_all_links()
    if len(all_links) != 175320:
        print("Warning: Not all links have been scraped!")
    if TESTING_FLAG:
        all_links = all_links[:50] 
    process_these_marc_urls(all_links)

if __name__ == "__main__":
    main()










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

def get_page_w_id(link):
    """ Returns photo info (as soup obj) and photo id string """
    new_link = re.sub("/collection/fsa", "", link)
    photo_id = re.sub(loc_url_prefix, "", link)
    photo_id = re.sub("/PP/", "", photo_id)
    this_soup = load_page_as_soup(new_link)
    return photo_id, this_soup



def main():
    """ Downloads the marc records for urls in pickle/all_urls.p """
    with open(base_path + "pickle/all_urls.p", 'r') as f:
        all_links = pickle.load(f)
    error_links = []
    while all_links:
        for link in all_links:
            photo_id, this_soup = get_page_w_id(link)
            if this_soup != None:
                with open(base_path + "img_url/" + photo_id + ".txt", 'w') as f:
                    these_urls = return_img_urls(this_soup, photo_id)
                    for url in these_urls: f.write(url + "\n")
                if verbose: print("Done with photo " + photo_id)        
            else:
                error_links.append(link)
        all_links = error_links


if __name__ == "__main__":
    main()

