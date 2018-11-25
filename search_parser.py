# -*- coding: UTF-8 -*-

import gobject
import json

class SearchParser:
    def __init__(self, gui):
        self.gui = gui

    def parse(self, response, is_videos):
        js = json.load(response)
        try:
            page_token = js["nextPageToken"]
        except:
            page_token = ""
        
        for item in js["items"]:
            if is_videos:
                video_id = item["id"]
            else:
                video_id = item["id"]["videoId"]
            gobject.idle_add(self.gui.add_to_results_model,
                             item["snippet"]["title"],
                             video_id,
                             item["snippet"]["thumbnails"]["default"]["url"])
                    
        return page_token
