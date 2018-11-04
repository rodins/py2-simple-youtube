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
        return f.read().strip()

API_KEY = get_api_key()

def build_search_link(query):
    API_DOMAIN = "https://www.googleapis.com/youtube/v3/search?"
    data = {}
    data['part'] = 'snippet'
    data['order'] = 'viewCount'
    data['maxResults'] = '15'
    data['q'] = query
    data['type'] = 'video'
    data['videoDefinition'] = 'standard'
    data['fields'] = 'items(id/videoId,snippet(thumbnails/default,title)),nextPageToken'
    data['key'] = API_KEY
    url_values = urllib.urlencode(data)
    return API_DOMAIN + url_values

def search_net(query):
    parser = SearchParser()    
    link = build_search_link(query)
    try:
        response = urllib2.urlopen(link)
        parser.parse(response)
    except Exception as ex:
        print ex

def main():
    search_net("house m.d")

if __name__ == "__main__":
    main()
