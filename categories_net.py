# -*- coding: UTF-8 -*-

import gobject

import urllib
import urllib2

from categories_parser import CategoriesParser

class CategoriesNet:
    def __init__(self, api_key, gui, loc):
        self.parser = CategoriesParser(gui)
        self.gui = gui
        self.API_DOMAIN = "https://www.googleapis.com/youtube/v3/videoCategories?"
        self.API_KEY = api_key
        try:
            locale = loc[0].split('_')
            self.language = locale[0]
            self.country = locale[1]
        except:
            self.language = ""
            self.country = ""

    def build_categories_link(self):
        data = {}
        data['part'] = 'snippet'
        if self.language != '':
            data['hl'] = self.language
        if self.country != '':
            data['regionCode'] = self.country
        data['fields'] = 'items(id,snippet(assignable,title))'
        data['key'] = self.API_KEY
        url_values = urllib.urlencode(data)
        return self.API_DOMAIN + url_values

    def get_results(self):
        link = self.build_categories_link()
        try:
            gobject.idle_add(self.gui.show_categories_loading_indicator)
            response = urllib2.urlopen(link)
            gobject.idle_add(self.gui.show_categories_data)
            self.parser.parse(response)
        except Exception as ex:
            gobject.idle_add(self.gui.show_categories_error)
            print ex

        
