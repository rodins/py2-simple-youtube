# -*- coding: UTF-8 -*-

import gobject

import urllib
import urllib2
import json

class ChannelNet:
    def __init__(self, api_key, gui):
        self.gui = gui
        self.API_DOMAIN = 'https://www.googleapis.com/youtube/v3/'
        self.VIDEOS = 'videos?'
        self.API_KEY = api_key
        self.video_id = ""

    def build_videos_url(self):
        data = {}
        data['part'] = 'snippet'
        data['id'] = self.video_id
        data['fields'] = 'items(snippet(channelId,channelTitle))'
        data['key'] = self.API_KEY
        url_values = urllib.urlencode(data)
        return self.API_DOMAIN + self.VIDEOS + url_values

    def parse(self, response):
        js = json.load(response)
        item = js['items'][0]
        channel_id = item['snippet']['channelId']
        channel_title = item['snippet']['channelTitle']
        gobject.idle_add(self.gui.get_search_data_by_channel_id,
                         channel_title,
                         channel_id)
        

    def get_results(self):
        if self.video_id != '':
            link = self.build_videos_url()
            try:
                gobject.idle_add(self.gui.show_channel_loading_indicator)
                response = urllib2.urlopen(link)
                gobject.idle_add(self.gui.show_list_channel_button)
                self.parse(response)
            except Exception as ex:
                gobject.idle_add(self.gui.show_error_channel_button)
                print ex
    
