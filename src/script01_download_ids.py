import os
import urllib
import re
import socket

from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup

# Global variables
testing = False
base_path = "/Users/tba3/Desktop/files/photogrammar/"

# Global settings
socket.setdefaulttimeout(10)

def download_grid_html(this_url):
    """ Downloads a local copy of this_url """
    url_prefix = "http://www.loc.gov/pictures/search/\?sp="
    url_suffix = "&co=fsa"
    save_to = re.sub(url_prefix, "", this_url)
    save_to = re.sub(url_suffix, "", save_to)
    save_to = base_path + "html/grid/" + save_to + ".html"
    try:
        if not os.path.exists(save_to):
            urllib.urlretrieve(this_url, save_to)
            return ""
        else: 
            return ""
    except IOError:
        return this_url
    except:
        return this_url


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

def get_these_pages_links(page_ids):
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

def check_id_files():
    """ Checks id files; deletes those with errors """
    finished_flag = True
    current_id_files = os.listdir(base_path + "photo_ids")
    for fname in current_id_files:
        fname_full = base_path + "photo_ids/" + fname
        size = os.stat(fname_full).st_size
        if size != 1320:
            if fname != "1.txt": # this page should be smaller
                org_name = base_path + "html/grid/" + fname
                org_name = re.sub("txt", "html", org_name)
                os.remove(org_name)
                os.remove(fname_full)
                finished_flag = False
    if len(current_id_files) != 8766: finished_flag = False
    return finished_flag

def main():
    url_prefix = "http://www.loc.gov/pictures/search/?sp="
    url_suffix = "&co=fsa"
    if not testing:
        index = range(1,8767)
    else:
        index = range(1,101)
    url_list = [url_prefix + str(x) + url_suffix for x in index]
    finished_flag = False
    while not finished_flag:
        # Try to download the urls which do not exist on filesystem
        pool = ThreadPool(processes=10)
        result = pool.map(download_grid_html, url_list)
        pool.close()
        del pool

        # Parse out file names using BeautifulSoup; save these
        if not testing:
            page_ids = os.listdir(base_path + "/html/grid")
        else:
            page_ids = os.listdir(base_path + "/html/grid")[:10]
        get_these_pages_links(page_ids)

        # Check ids and delete bad entries
        finished_flag = check_id_files()


if __name__ == "__main__":
    main()

