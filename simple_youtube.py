#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import gobject

import os
import sys

from simple_youtube_gui import Gui

def get_api_key():
    API_KEY_FILE = os.path.join(sys.path[0], "youtubeApiKey.txt")
    with open(API_KEY_FILE, "r") as f:
        return f.read().strip()

API_KEY = get_api_key()

def main():
    gobject.threads_init()
    Gui(API_KEY)
    gtk.main()

if __name__ == "__main__":
    main()
