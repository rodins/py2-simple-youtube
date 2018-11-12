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
        self.page_token = ""
        self.query = ""

    def set_query(self, query):
        self.query = query
        self.page_token = ""
        
    def build_search_link(self):
        data = {}
        data['part'] = 'snippet'
        data['order'] = 'date'
        data['maxResults'] = '15'
        data['q'] = self.query
        data['type'] = 'video'
        #thumbnails/medium/url default
        data['fields'] = 'items(id/videoId,snippet(thumbnails/default/url,title)),nextPageToken'
        data['key'] = self.API_KEY
        if self.page_token != "":
            data['pageToken'] = self.page_token
        url_values = urllib.urlencode(data)
        return self.API_DOMAIN + url_values

    def get_results(self):
        if self.query != "" and self.API_KEY != "":
            link = self.build_search_link()
            is_paging = (self.page_token != "")
            try:
                gobject.idle_add(self.gui.show_results_loading_indicator,
                                 is_paging)
                response = urllib2.urlopen(link)
                gobject.idle_add(self.gui.show_results_data)
                self.page_token = self.parser.parse(response)
            except Exception as ex:
                gobject.idle_add(self.gui.show_results_error, is_paging)
                print ex
            gobject.idle_add(self.gui.set_task_stopped)
