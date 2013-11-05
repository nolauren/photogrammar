#!/usr/bin/env python
""" Takes individual csv marc records and creates a single table

Provides functionality to grab additional variables
"""

import os
import urllib
import re
import socket
import copy
import pandas as pd

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

class MarcClassificationFormat(object):
    def __init__(self, val1, val2 = "", val3 = "", val4 = ""):
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3
        self.val4 = val4
    def get_attr(self, mr_obj):
        bool_df = (mr_obj.data.val1 == self.val1) & \
                  (mr_obj.data.val2 == self.val2) & \
                  (mr_obj.data.val3 == self.val3) & \
                  (mr_obj.data.val4 == self.val4)
        these = mr_obj.data[bool_df].text
        if len(these) == 1:
            return(list(these)[0])
        elif len(these) == 0:
            return ""
        else:
            raise ValueError("Non-unique rows specified")

class MarcRecord(object):
    def __init__(self, path):
        self.path = path
        data = pd.read_csv(path, header=None, dtype=str,
                   names=['val1', 'val2', 'val3', 'val4', 'text'])
        regex = re.compile('( )|(\xc2\xa0)')
        for iter in range(len(data.val1)):      
            if pd.isnull(data.val1[iter]):
                data.val1[iter] = data.val1[iter - 1]
        data.val1 = [re.sub(regex, '', x) for x in data.val1]
        data.val2 = [re.sub(regex, '', x) for x in data.val2]
        data.val3 = [re.sub(regex, '', x) for x in data.val3]
        data.val4 = [re.sub(regex, '', x) for x in data.val4]
        self.data = data

data = MarcRecord("/Users/tba3/Desktop/files/photogrammar/marc_records/fsa1997000005.csv")

cat_num = MarcClassificationFormat(val1="037", val4="a")
photographer = MarcClassificationFormat(val1="100", val2="1", val4="a")

cat_num.get_attr(data)
photographer.get_attr(data)



def main():
    """ Downloads the marc records for urls in pickle/all_urls.p """
    pass


if __name__ == "__main__":
    main()

