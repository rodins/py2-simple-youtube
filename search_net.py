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
        self.video_id = ""
        self.channel_id = ""
        try:
            locale = loc[0].split('_')
            self.language = locale[0]
            self.country = locale[1]
        except:
            self.language = ""
            self.country = ""
        self.order = 'date'

    def clear(self):
        self.query = ""
        self.video_id = ""
        self.category_id = ""
        self.channel_id = ""
            
    def set_query(self, query):
        self.clear()
        self.query = query

    def set_category_id(self, category_id):
        self.clear()
        self.category_id = category_id

    def set_video_id(self, video_id):
        self.clear()
        self.video_id = video_id

    def set_channel_id(self, channel_id):
        self.clear()
        self.channel_id = channel_id

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
        data['maxResults'] = self.max_results
        if self.query != '':
            data['q'] = self.query
            data['order'] = self.order
        if self.video_id != '':
            data['relatedToVideoId'] = self.video_id
        if self.channel_id != '':
            data['channelId'] = self.channel_id
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
            # TODO: change this if condition
            if self.query != '' or self.video_id != '' or self.channel_id != '':
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
