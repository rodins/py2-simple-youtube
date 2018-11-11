# -*- coding: UTF-8 -*-
import os
import subprocess
from subprocess import Popen
import gobject

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

    def get_direct_link(self):
        try:
            print "Getting link..."
            link = subprocess.check_output(
                ["youtube-dl -g -f "+self.resolution_code+" "+self.video_id],
                shell=True)
            print "Starting player..."
            gobject.idle_add(self.play, link.strip('\n'))
        except Exception as ex:
            print ex

    def play(self, link):
        if self.player == "omxplayer":
            subprocess.call(
            ["lxterminal -e omxplayer -b \"" + link + "\" &"], shell=True)
        elif self.player != "":
            subprocess.call([self.player + " " + link + " &"],
                            shell=True)
        else:
            print "TODO: Show error dialog - no player detected"
        print "Player started"
            
        
 
