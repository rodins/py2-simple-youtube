# -*- coding: UTF-8 -*-

import threading

class ResolutionsTask(threading.Thread):
    def __init__(self, processor):
         self.processor = processor
         threading.Thread.__init__(self)

    def run(self):
        self.processor.process()
