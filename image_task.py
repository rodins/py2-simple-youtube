# -*- coding: UTF-8 -*-

import gtk
import gobject

import threading
import urllib2

class ImageTask(threading.Thread):
    def __init__(self, link, row, images_cache):
        self.images_cache = images_cache
        self.link = link
        self.row = row
        self.pixbuf_loader = gtk.gdk.PixbufLoader()
        self.pixbuf_loader.connect("area-prepared", self.pixbuf_loader_prepared)
        self.is_cancelled = False
        threading.Thread.__init__(self)
        
    def pixbuf_loader_prepared(self, pixbufloader):
        self.row[0] = pixbufloader.get_pixbuf()
        
    def write_to_loader(self, buf):
        self.pixbuf_loader.write(buf)
        
    def on_post_execute(self):
        if self.pixbuf_loader.close():
            pixbuf = self.pixbuf_loader.get_pixbuf()
            self.images_cache[self.link] = pixbuf
            self.row[0] = pixbuf
        else:
            print "pixbuf error"
        
    def cancel(self):
        self.is_cancelled = True
        
    def run(self):
        try:
            response = urllib2.urlopen(self.link)
            for buf in response:
                if self.is_cancelled:
                    break 
                gobject.idle_add(self.write_to_loader, buf)
        except Exception as ex:
            print ex
        gobject.idle_add(self.on_post_execute)
