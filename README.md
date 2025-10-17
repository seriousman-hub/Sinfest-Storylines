# Sinfest-Storylines

This project downloads all comics from sinfest.xyz and organizes them into folders based upon storylines. It also organizes all storylines by year.

There are two components: scraper.py and folders.py

scraper.py generates a list of all sinfest comics and finds the keywords used on the website. The keywords are used in folders.py to try and group extended storylines that go under multiple names.
scraper.py generates the file ComicList.txt. ComicList.txt is a delimited text file using '|'.

folders.py downloads and sorts the comics. folders.py needs ComicList.txt to run.

**Setup**

To run this project on your computer, put ComicList.txt and folders.py into the same folder. Then create a subfolder named "Output". This is where all the comics will go.
scraper.py is not necessary unless you want to update ComicList.txt.

Once the folder is setup, run folders.py. folders.py needs the requests, re, and os packages in order to run.
