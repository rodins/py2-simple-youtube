# -*- coding: UTF-8 -*-

import subprocess
from subprocess import Popen
import gobject
import urllib2

class Player:
    def __init__(self, gui):
        self.gui = gui
        self.player = ""
        players = ["mpv", "omxplayer", "vlc", "mplayer"]
        resolutions = {}
        for player in players:
            try:
                subprocess.check_call(["which", player])
                self.player = player
                self.gui.set_player_init_text("Detected: " + player)
                break
            except:
                self.gui.set_player_init_text("Not detected")
        try:
            subprocess.check_call(["which", "nostreamlink"])
            self.streamlink = "streamlink"
        except Exception as ex:
            print ex
            self.streamlink = ""
        
            
    def set_link(self, video_id, title, res):
        self.video_id = video_id
        self.title = title
        self.res = res

    def get_direct_link(self):
        try:
            gobject.idle_add(self.gui.set_player_text, "Getting link...")
            link = subprocess.check_output(
                ["youtube-dl -g -f "+self.res+" "+"http://youtu.be/"+self.video_id],
                shell=True)
            if link.find(".m3u8") != -1:
                if self.streamlink != "":
                    gobject.idle_add(self.gui.set_player_text,
                                     "Starting streamlink...")
                    gobject.idle_add(self.play_stream,
                                     self.title.split("x")[1] + "p")
                else:
                    gobject.idle_add(self.gui.set_player_text,
                                     "Need streamlink to play this")
            else:
                gobject.idle_add(self.play, link.strip('\n'))
        except Exception as ex:
            print ex

    def play(self, link):
        if self.player == "":
            return
        if self.player == "omxplayer":
            subprocess.call(
            ["lxterminal -e omxplayer -b \"" + link + "\" &"],
            shell=True)
        else:
            subprocess.call([self.player + " \"" + link + "\" &"],
                            shell=True)
        gobject.idle_add(self.gui.set_player_text,
                         "Player started")

    def play_stream(self, res):
        if self.player == "":
            return
        if self.player == "omxplayer":
            subprocess.call(
            ["lxterminal -e "+self.streamlink+" -p \"omxplayer -b\" --player-fifo http://youtu.be/"+self.video_id+" "+res+" &"],
            shell=True)
        else:
            subprocess.call(
            [self.streamlink+" -p "+self.player+" --player-fifo http://youtu.be/"+self.video_id+" "+res+" &"],
            shell=True)
        gobject.idle_add(self.gui.set_player_text,
                         "Streamlink started")
        
 
