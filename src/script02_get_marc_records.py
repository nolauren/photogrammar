#!/usr/bin/env python
""" Downloads the marc records for all 175320 photos in the collection

Using the photo ids obtained in script01, this downloads and parses
all of the marc records as csv files. Saves a copy of the html files
locally, as the webscrape can take quite a while. Uses threading with
10 threads (more is faster, but can result in a temporary ip block
with the LOC site)
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
__version__  = "0.1.3"

def get_all_links():
    """ Reads files in photo_ids and returns every available url """
    current_id_files = os.listdir(BASE_PATH + "photo_ids")
    current_id_files = [BASE_PATH + "photo_ids/" + x for x in current_id_files]
    all_links = []
    for file in current_id_files:
        with open(file, 'r') as f:
            x = f.read()
            all_links += x.split("\n")[:20]
    return all_links

def download_marc_html(this_link_url):
    """ Downloads a local copy of the marc record matching this_link_url

    The output is saved as an html file on disk in html/marc.
    """
    # Convert url (which is to the info page) into 
    loc_url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"
    new_link = re.sub("/collection/fsa", "", this_link_url) + "marc/"
    url_prefix = "http://www.loc.gov/pictures/item/"
    url_suffix = "/PP/marc/"

    # Construct the output file name
    save_to = re.sub(url_prefix, "", new_link)
    save_to = re.sub(url_suffix, "", save_to)
    save_to = re.sub("/marc/", "", save_to)
    save_to = BASE_PATH + "html/marc/" + save_to + ".html"

    try:
        if not os.path.exists(save_to):
            urllib.urlretrieve(new_link, save_to)
        else: 
            pass
    except IOError:
        pass
    except:
        pass

def save_marc_record(this_file):
    """ Turns marc webpage into a csv file and writes to disk

    The input this_file should be the file name of a downloaded
    marc record; a csv file will be written to disk in marc_records
    as a csv file.
    """
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
    """ Checks that there exists a marc record csv for every file in all_links

    The function returns, in the same format, the subset of all_links which
    have not yet been properly created as a csv file.
    """
    finished_marc_records = os.listdir(BASE_PATH + "marc_records")
    all_links_names = []
    url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"
    url_suffix = "/PP"
    for link in all_links:
        regex = re.compile("("+url_prefix+")|("+url_suffix+")|(/marc/)|(/)") 
        link = re.sub(regex, "", link)
        all_links_names.append(link + ".csv")
    set_diff = list(set(all_links_names) - set(finished_marc_records))
    set_diff = [re.sub("\.csv", "", x) for x in set_diff]
    set_diff = [url_prefix + x + url_suffix + "/" for x in set_diff] 
    return set_diff

def process_these_marc_urls(links):
    """ Process all raw marc urls in 'links' """
    these_links = copy.copy(links)
    while these_links:
        # Download a local copy of the marc record html files
        pool = ThreadPool(processes=5)
        pool.map(download_marc_html, these_links)
        pool.close()
        del pool

        # Parse marc html files; save as csv
        marc_files = os.listdir(BASE_PATH + "/html/marc")
        for this_file in marc_files:
            save_marc_record(this_file)

        # Check if all records in all_links are parsed
        these_links = check_records(links)

def main():
    """ Run all marc records or a test set of these """
    all_links = get_all_links()
    if len(all_links) != 175320:
        print("Warning: Not all links have been scraped!")
    if TESTING_FLAG:
        all_links = all_links[:50] 
    process_these_marc_urls(all_links)

if __name__ == "__main__":
    main()



