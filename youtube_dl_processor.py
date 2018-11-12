# -*- coding: UTF-8 -*-

import gobject
import subprocess

from simple_youtube_player import Player
from player_task import PlayerTask

class VideoIdProcessor:
    def __init__(self, gui):
        self.gui = gui
        self.player = Player(gui)
        self.video_id = ""
        try:
            subprocess.check_call(["which", "youtube-dl"])
            self.youtube_dl = "youtube-dl"
        except Exception as ex:
            print ex
            self.youtube_dl = ""

    def process(self):
        if self.youtube_dl != "":
            try:
                gobject.idle_add(self.gui.show_resolutions_loading_indicator)
                formats = subprocess.check_output(
                    [self.youtube_dl + " -F " + "youtu.be/" + self.video_id],
                    shell=True)
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
            gobject.idle_add(self.gui.set_player_text,
                             "No youtube-dl detected")
            
    def play(self, title, res):
        self.player.set_link(self.video_id, title, res)
        task = PlayerTask(self.player)
        task.start()
        
            
        
