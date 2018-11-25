# -*- coding: UTF-8 -*-

import gobject
import json

class CategoriesParser:
    def __init__(self, gui):
        self.gui = gui
        self.is_empty = True

    def parse(self, response):
        js = json.load(response)
        for item in js["items"]:
            assignable = item['snippet']['assignable']
            # Click on assignable false category gives error
            if assignable:
                self.is_empty = False
                gobject.idle_add(self.gui.add_to_categories_model,
                                 item['snippet']['title'],
                                 item['id'])
