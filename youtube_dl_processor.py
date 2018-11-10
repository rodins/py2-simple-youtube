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
            try:
                print "Getting formats..."
                formats = subprocess.check_output(
                    [self.youtube_dl + " -F " + video_id], shell=True)
                for line in formats.splitlines():
                    if (line.find("only") == -1
                    and line.find(video_id) == -1
                    and line.find("format") == -1):
                        #print line
                        columns = line.split()
                        title = columns[1] + " " + columns[2]
                        print title
                        print columns[0]
            except Exception as ex:
                print ex
            #self.player.play_link(video_id)
        else:
            print "TODO: show error dialog no youtube-dl installed"
            
            
