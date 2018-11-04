# -*- coding: UTF-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import gobject

class Gui(gtk.Window):
    def __init__(self):
        super(Gui, self).__init__()
        
        self.connect("destroy", self.on_destroy)
        self.set_border_width(5)
        self.set_size_request(700, 400)
        #TODO: add app icon

        
        self.show()

    def on_destroy(self, widget):
        gtk.main_quit()
