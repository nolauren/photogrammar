import os
import urllib
import re
import socket
import copy

from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup


# Global variables
testing = False
base_path = "/Users/tba3/Desktop/files/photogrammar/"

# Global settings
socket.setdefaulttimeout(10)

def get_all_links():
    """ Reads files in photo_ids; returns every available url """
    current_id_files = os.listdir(base_path + "photo_ids")
    current_id_files = [base_path + "photo_ids/" + x for x in current_id_files]
    all_links = []
    for file in current_id_files:
        with open(file, 'r') as f:
            x = f.read()
            all_links += x.split("\n")[:20]
    return all_links

def download_marc_html(this_url):
    """ Downloads a local copy of this_url """
    url_prefix = "http://www.loc.gov/pictures/item/"
    url_suffix = "/PP/marc/"
    save_to = re.sub(url_prefix, "", this_url)
    save_to = re.sub(url_suffix, "", save_to)
    save_to = re.sub("/marc/", "", save_to)
    save_to = base_path + "html/marc/" + save_to + ".html"
    try:
        if not os.path.exists(save_to):
            urllib.urlretrieve(this_url, save_to)
        else: 
            pass
    except IOError:
        pass
    except:
        pass

def get_marc_w_id(link):
    """ Returns mark records (as soup obj) and photo id string """
    loc_url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"
    new_link = re.sub("/collection/fsa", "", link) + "marc/"
    download_marc_html(new_link)
    return 0

def save_marc_record(this_file):
    """ Turns mark webpage into a csv file and writes to disk """
    path_prefix = base_path + "marc_records/"
    file_out = path_prefix + re.sub("\.html", ".csv", this_file)
    if not os.path.exists(file_out):
        with open(base_path + "html/marc/" + this_file) as g:
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
    finished_marc_records = os.listdir(base_path + "marc_records")
    all_links_names = []
    url_prefix = "http://www.loc.gov/pictures/collection/fsa/item/"
    url_suffix = "/PP"
    for link in all_links:
        link = re.sub(url_prefix, "", link)
        link = re.sub(url_suffix, "", link)
        link = re.sub("/marc/", "", link)
        link = re.sub("/", "", link)
        all_links_names.append(link + ".csv")
    return list(set(all_links_names) - set(finished_marc_records))

def main():
    """ Downloads the marc records and saves as csv files """
    all_links = get_all_links()
    if len(all_links) != 175320:
        print("Warning: Not all links have been successfully scraped!")
    if testing:
        all_links = all_links[:50]   
    these_links = copy.copy(all_links)
    while these_links:
        # Download a local copy of the marc record html files
        pool = ThreadPool(processes=10)
        result = pool.map(get_marc_w_id, these_links)
        pool.close()
        del pool

        # Parse marc html files; save as csv
        marc_files = os.listdir(base_path + "/html/marc")
        for this_file in marc_files:
            save_marc_record(this_file)

        # Check if all records in all_links are parsed
        these_links = check_records(all_links)


if __name__ == "__main__":
    main()



