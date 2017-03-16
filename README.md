photogrammar
============

Code for getting and exploring the photogrammar data.

For example, we download a list of all the photo ids (these uniquely define
the urls for scraping the rest of the data, by running the following code:

```shell
python src/get_photo_ids.py
```
This creates a file pickle/all_urls.p, a python pickle file. Now we can run the code to download MARC records
from the Library of Congress website for all photo ids in the all_urls.p file. This is done by:
```shell
python src/get_marc_records.py
```
When finished, there should be files in the marc_records directory, such as 'marc_recordsfsa1997000988.csv'.
Now, to finish the first stage of the scrape, we download the image urls using a similar syntax:
```shell
python src/get_img_urls.py
```
Which will create text files in the directory 'img_url' such as 'img_url/fsa1997000987.txt' which contain the urls
of the photo images. 

**

