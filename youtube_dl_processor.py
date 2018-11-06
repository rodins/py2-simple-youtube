# -*- coding: UTF-8 -*-

import os
import subprocess
from simple_youtube_player import Player

class VideoIdProcessor:
    def __init__(self):
        self.player = Player()
        if os.system("which youtube-dl") == 0:
            self.youtube_dl = "youtube-dl"
        else:
            self.youtube_dl = ""
    
    def process(self, video_id):
        if self.youtube_dl != "":
            self.player.play_link(video_id)
        else:
            print "TODO: show error dialog no youtube-dl installed"
            
            
