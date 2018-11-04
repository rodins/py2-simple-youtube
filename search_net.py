# -*- coding: UTF-8 -*-

import urllib
import urllib2

from search_parser import SearchParser

class SearchNet:
    def __init__(self, api_key):
        self.parser = SearchParser()
        self.API_DOMAIN = "https://www.googleapis.com/youtube/v3/search?"
        self.API_KEY = api_key

    def build_search_link(self, query):
        data = {}
        data['part'] = 'snippet'
        data['order'] = 'viewCount'
        data['maxResults'] = '15'
        data['q'] = query
        data['type'] = 'video'
        data['videoDefinition'] = 'standard'
        data['fields'] = 'items(id/videoId,snippet(thumbnails/default,title)),nextPageToken'
        data['key'] = self.API_KEY
        url_values = urllib.urlencode(data)
        return self.API_DOMAIN + url_values

    def get_results(self, query):   
        link = self.build_search_link(query)
        try:
            response = urllib2.urlopen(link)
            self.parser.parse(response)
        except Exception as ex:
            print ex
