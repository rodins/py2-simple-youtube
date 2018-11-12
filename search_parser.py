# -*- coding: UTF-8 -*-

import gobject
import json

class SearchParser:
    def __init__(self, gui):
        self.gui = gui

    def parse(self, response):
        js = json.load(response)
        try:
            page_token = js["nextPageToken"]
        except:
            page_token = ""
        
        for item in js["items"]:
            gobject.idle_add(self.gui.add_to_results_model,
                             item["snippet"]["title"],
                             item["id"]["videoId"],
                             item["snippet"]["thumbnails"]["default"]["url"])
                    
        return page_token
