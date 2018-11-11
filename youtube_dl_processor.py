# -*- coding: UTF-8 -*-

import gobject
import os
import subprocess
from simple_youtube_player import Player
from player_task import PlayerTask

class VideoIdProcessor:
    def __init__(self, gui):
        self.gui = gui
        self.player = Player()
        self.video_id = ""
        if os.system("which youtube-dl") == 0:
            self.youtube_dl = "youtube-dl"
        else:
            self.youtube_dl = ""
    
    def process(self):
        if self.youtube_dl != "":
            try:
                gobject.idle_add(self.gui.show_resolutions_loading_indicator)
                formats = subprocess.check_output(
                    [self.youtube_dl + " -F " + self.video_id], shell=True)
                gobject.idle_add(self.gui.show_resolutions_data)
                for line in formats.splitlines():
                    if (line.find("only") == -1
                    and line.find(self.video_id) == -1
                    and line.find("format") == -1):
                        columns = line.split()
                        title = columns[1] + " " + columns[2]
                        gobject.idle_add(self.gui.add_to_resolutions_model,
                                         title,
                                         columns[0])
            except Exception as ex:
                print ex
                gobject.idle_add(self.gui.show_resolutions_error)
            
        else:
            print "TODO: show error dialog no youtube-dl installed"
            
    def play(self, resolution_code):
        self.player.set_link(self.video_id, resolution_code)
        #self.player.play()
        task = PlayerTask(self.player)
        task.start()
        
