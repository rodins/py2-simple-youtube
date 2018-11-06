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

    def play_link(self, link):
        if self.player == "omxplayer":
            try:
                subprocess.call(
                ["lxterminal -e omxplayer -b $(youtube-dl -g -f 18 " + link + ")"],
                shell=True)
            except Exception as ex:
                print ex
        elif self.player != "":
            Popen([self.player, link])
        else:
            print "TODO: Show error dialog - no player detected"
 
