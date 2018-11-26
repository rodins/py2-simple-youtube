# -*- coding: UTF-8 -*-

import gobject

import urllib
import urllib2

from search_parser import SearchParser

class SearchNet:
    def __init__(self, api_key, gui, loc):
        self.parser = SearchParser(gui)
        self.gui = gui
        self.API_DOMAIN = 'https://www.googleapis.com/youtube/v3/'
        self.SEARCH = 'search?'
        self.VIDEOS = 'videos?'
        self.max_results = '15'
        self.API_KEY = api_key
        self.page_token = ""
        self.query = ""
        self.category_id = ""
        try:
            locale = loc[0].split('_')
            self.language = locale[0]
            self.country = locale[1]
        except:
            self.language = ""
            self.country = ""
        self.order = 'date'
            
    def set_query(self, query):
        self.query = query
        self.category_id = ""
        self.page_token = ""

    def set_category_id(self, category_id):
        self.query = ""
        self.category_id = category_id
        self.page_token = ""

    def build_videos_url(self):
        data = {}
        data['part'] = 'snippet'
        data['chart'] = 'mostPopular'
        data['maxResults'] = self.max_results
        if self.category_id != '':
            data['videoCategoryId'] = self.category_id
        if self.language != "":
            data['hl'] = self.language
        if self.country != "":
            data['regionCode'] = self.country
        #thumbnails/medium/url default
        data['fields'] = 'items(id,snippet(thumbnails/default/url,title)),nextPageToken'
        data['key'] = self.API_KEY
        if self.page_token != "":
            data['pageToken'] = self.page_token
        url_values = urllib.urlencode(data)
        return self.API_DOMAIN + self.VIDEOS + url_values
        
    def build_search_url(self):
        data = {}
        data['part'] = 'snippet'
        data['order'] = self.order
        data['maxResults'] = self.max_results
        data['q'] = self.query
        data['type'] = 'video'
        if self.language != "":
            data['relevanceLanguage'] = self.language
        if self.country != "":
            data['regionCode'] = self.country
        #thumbnails/medium/url default
        data['fields'] = 'items(id/videoId,snippet(thumbnails/default/url,title)),nextPageToken'
        data['key'] = self.API_KEY
        if self.page_token != "":
            data['pageToken'] = self.page_token
        url_values = urllib.urlencode(data)
        return self.API_DOMAIN + self.SEARCH + url_values

    def get_results(self):
        if self.API_KEY != "":
            if self.query != "":
                link = self.build_search_url()
                is_videos = False
            else:
                link = self.build_videos_url()
                is_videos = True
            is_paging = (self.page_token != "")
            try:
                gobject.idle_add(self.gui.show_results_loading_indicator,
                                 is_paging)
                response = urllib2.urlopen(link)
                gobject.idle_add(self.gui.show_results_data)
                self.page_token = self.parser.parse(response, is_videos)
            except Exception as ex:
                gobject.idle_add(self.gui.show_results_error, is_paging)
                print ex
            gobject.idle_add(self.gui.set_task_stopped)
