# -*- coding: UTF-8 -*-
import threading

class SearchTask(threading.Thread):
    def __init__(self, search_net, query):
         self.search_net = search_net
         self.query = query
         threading.Thread.__init__(self)

    def run(self):
        self.search_net.get_results(self.query)
    
