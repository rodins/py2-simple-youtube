# -*- coding: UTF-8 -*-

import threading

class ResolutionsTask(threading.Thread):
    def __init__(self, processor):
         self.processor = processor
         threading.Thread.__init__(self)

    def run(self):
        if self.is_ytdl:
            self.processor.process_ytdl()
        else:
            self.processor.process_streamlink()
