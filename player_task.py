# -*- coding: UTF-8 -*-
import threading

class PlayerTask(threading.Thread):
    def __init__(self, player):
         self.player = player
         threading.Thread.__init__(self)

    def run(self):
        self.player.get_direct_link()
