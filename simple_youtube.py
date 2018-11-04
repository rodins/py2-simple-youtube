#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import urllib
import urllib2

from search_parser import SearchParser

def get_api_key():
    API_KEY_FILE = os.path.join(sys.path[0], "youtubeApiKey.txt")
    with open(API_KEY_FILE, "r") as f:
        return f.read()

API_KEY = get_api_key()

def search_net(query):
    parser = SearchParser()
    query = urllib.quote(query)
    link = "https://www.googleapis.com/youtube/v3/search?part=snippet&order=viewCount&pageToken=15&q=" + query + "&type=video&videoDefinition=standard&fields=items(id%2FvideoId%2Csnippet(thumbnails%2Fdefault%2Ctitle))%2CnextPageToken&key=" + API_KEY
    try:
        response = urllib2.urlopen(link)
        parser.parse(response)
    except Exception as ex:
        print ex

def main():
    search_net("house m.d")

if __name__ == "__main__":
    main()
