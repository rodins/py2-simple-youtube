# -*- coding: UTF-8 -*-
import os
import subprocess
from subprocess import Popen

class Player:
    def __init__(self):
        self.player = ""
        players = ["mpv", "omxplayer", "mplayer"]
        for player in players:
            if os.system("which " + player) == 0:
                self.player = player
                break
    def set_link(self, video_id, resolution_code):
        self.video_id = video_id
        self.resolution_code = resolution_code

    def play(self):
        try:
            youtube_dl=" $(youtube-dl -g -f "+self.resolution_code+" "+self.video_id+")"
            print youtube_dl
            if self.player == "omxplayer":
                subprocess.call(
                ["lxterminal -e omxplayer -b" + youtube_dl + " &"], shell=True)
            elif self.player != "":
                subprocess.call([self.player + youtube_dl + " &"], shell=True)
            else:
                print "TODO: Show error dialog - no player detected"
        except Exception, ex:
            print ex
        
 
