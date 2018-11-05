# -*- coding: UTF-8 -*-

import gobject

class SearchParser:
    def __init__(self, gui):
        self.gui = gui

    def find_value(self, key, line):
        offset = len(key)+4
        begin = line.find(key)
        end = line.find("\"", begin+offset+1)
        if begin != -1 and end != -1:
            value = line[begin+offset:end]
            return value
        else:
            return ""

    def parse(self, response):
        is_item = False
        for line in response:
            value = self.find_value("nextPageToken", line)
            if value != "":
                next_page = value
                continue

            value = self.find_value("videoId", line)
            if value != "":
                is_item = True
                video_id = value
                continue
            value = self.find_value("title", line)
            if value != "":
                title = value
                continue
            value = self.find_value("url", line)
            if value != "":
                image_url = value
                if is_item:
                    is_item = False
                    gobject.idle_add(self.gui.add_to_results_model,
                                     title,
                                     video_id,
                                     image_url)
        gobject.idle_add(self.gui.set_next_page, next_page)
