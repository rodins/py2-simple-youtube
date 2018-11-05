# -*- coding: UTF-8 -*-

import gobject

import urllib
import urllib2

from search_parser import SearchParser

class SearchNet:
    def __init__(self, api_key, gui):
        self.parser = SearchParser(gui)
        self.gui = gui
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
            gobject.idle_add(self.gui.show_results_loading_indicator, False)
            response = urllib2.urlopen(link)
            gobject.idle_add(self.gui.show_results_data)
            self.parser.parse(response)
        except Exception as ex:
            gobject.idle_add(self.gui.show_results_error, False)
            print ex
