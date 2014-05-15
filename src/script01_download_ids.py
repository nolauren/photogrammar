#!/usr/bin/env python
""" Downloads the 'grid' index of the records in the fsa/owi collection

This script cycles through the 8766 pages of the fsa/owi collection index
on the LOC site. These html files contain the unique photo id codes
which identify the marc record and image urls. The script downloads a
local version of each page and then parses each one into a simple text
file with 20 lines each, one for each record in the collection. Due to
inevitable network issues, the script checks each page and re-downloads
those the do not return all 20 records.
"""

import os
import urllib
import re
import socket
import logging

from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup

# Global variables; define defaults when invoking as script
TESTING_FLAG = False
BASE_PATH = "/Users/tba3/Desktop/files/photogrammar/"

# Meta data
__author__ = "Taylor B. Arnold"
__date__ = "3 November 2013"
__contact__ = "taylor.b.arnold <at> gmail.com"
__version__ = "0.1.3"

# Logging
logging.basicConfig(level=logging.DEBUG)


def download_grid_html(input_tuple):
    """ Downloads a local copy of this_url """
    this_url, base_path = input_tuple
    url_prefix = "http://www.loc.gov/pictures/search/\?sp="
    url_suffix = "&co=fsa"
    save_to = re.sub(url_prefix, "", this_url)
    save_to = re.sub(url_suffix, "", save_to)
    save_to = base_path + "html/grid/" + save_to + ".html"
    try:
        if not os.path.exists(save_to):
            urllib.urlretrieve(this_url, save_to)
        else:
            pass
    except IOError:
        pass
    except:
        pass


def load_file_as_soup(file_name):
    """ Loads file in as a soup obj """
    with open(file_name, 'r') as f:
        s = f.read()
        soup = BeautifulSoup(s)
    return soup


def get_this_page_links(soup_obj):
    """ Takes a soup object and extracts photo page urls  """
    loc_url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"
    output = []
    for link in soup_obj.find_all('a', attrs={"class": None}):
        this_link = link.get('href', default="")
        if re.match(loc_url_prefix, this_link):
            output.append(this_link)
    return output


def get_these_pages_links(page_ids, base_path):
    """ Takes local html file and extracts urls / ids from them """
    for fname in page_ids:
        file_name = base_path + "html/grid/" + fname
        file_name_out = base_path + "photo_ids/" + fname
        file_name_out = re.sub('html', 'txt', file_name_out)
        if not os.path.exists(file_name_out):
            this_soup = load_file_as_soup(file_name)
            items = get_this_page_links(this_soup)
            with open(file_name_out, 'w') as f:
                for item in items:
                    f.write(item)
                    f.write("\n")


def check_id_files(base_path):
    """ Checks id files; deletes those with errors """
    finished_flag = True
    current_id_files = os.listdir(base_path + "photo_ids")
    for fname in current_id_files:
        fname_full = base_path + "photo_ids/" + fname
        size = os.stat(fname_full).st_size
        if size != 1320:
            if fname != "1.txt":  # this page should be smaller
                org_name = base_path + "html/grid/" + fname
                org_name = re.sub("txt", "html", org_name)
                os.remove(org_name)
                os.remove(fname_full)
                finished_flag = False
    if len(current_id_files) != 8766:
        finished_flag = False
    return finished_flag


def process_these_id_urls(index_list, testing_flag, base_path):
    """ Process all indicies given in index_list; number  1-8966 """
    url_prefix = "http://www.loc.gov/pictures/search/?sp="
    url_suffix = "&co=fsa"
    url_list = [url_prefix + str(x) + url_suffix for x in index_list]
    url_list = [(x, base_path) for x in url_list]
    finished_flag = False
    while not finished_flag:
        # Try to download the current set of urls
        pool = ThreadPool(processes=10)
        socket.setdefaulttimeout(10)
        pool.map(download_grid_html, url_list)
        pool.close()
        del pool

        # Parse out file names using BeautifulSoup and save
        page_ids = os.listdir(base_path + "/html/grid")
        get_these_pages_links(page_ids, base_path)

        # Check ids and delete bad entries
        finished_flag = check_id_files(base_path)


def main(testing_flag, base_path):
    """ Run either all indicies or test index """
    if not testing_flag:
        index = range(1, 8767)
    else:
        index = range(1, 101)
    process_these_id_urls(index, testing_flag, base_path)


if __name__ == "__main__":
    main(TESTING_FLAG, BASE_PATH)
