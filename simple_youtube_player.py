# -*- coding: UTF-8 -*-

import subprocess
from subprocess import Popen
import gobject
import urllib2

class Player:
    def __init__(self):
        self.player = ""
        players = ["mpv", "omxplayer", "mplayer"]
        resolutions = {}
        for player in players:
            try:
                subprocess.check_call(["which", player])
                self.player = player
                break
            except Exception as ex:
                print ex
        try:
            subprocess.check_call(["which", "streamlink"])
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
            print "Getting link..."
            link = subprocess.check_output(
                ["youtube-dl -g -f "+self.res+" "+self.video_id],
                shell=True)
            if link.find(".m3u8") != -1:
                if self.streamlink != "":
                    print "Starting streamlink..."
                    gobject.idle_add(self.play_stream,
                                     self.title.split("x")[1] + "p")
                else:
                    print "Need streamlink to play this"
            else:
                print "Starting player..."
                gobject.idle_add(self.play, link.strip('\n'))
        except Exception as ex:
            print ex

    def play(self, link):
        if self.player == "omxplayer":
            subprocess.call(
            ["lxterminal -e omxplayer -b \"" + link + "\" &"],
            shell=True)
        elif self.player != "":
            subprocess.call([self.player + " \"" + link + "\" &"],
                            shell=True)
        else:
            print "TODO: Show error dialog - no player detected"
        print "Player started"

    def play_stream(self, res):
        if self.player == "omxplayer":
            subprocess.call(
            ["lxterminal -e "+self.streamlink+" -p \"omxplayer -b\" --player-fifo youtu.be/"+self.video_id+" "+res+" &"],
            shell=True)
        elif self.player != "":
            subprocess.call(
            ["lxterminal -e "+self.streamlink+" -p "+self.player+" --player-fifo youtu.be/"+self.video_id+" "+res+" &"],
            shell=True)
        else:
            print "TODO: Show error dialog - no player detected"
        print "Streamlink started"
        
 
