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

        # Toolbar and it's items
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        entry_item = gtk.ToolItem()
        entry = gtk.Entry()
        entry.set_tooltip_text("Search youtube")
        entry.connect("activate", self.entry_activated)
        entry_item.add(entry)
        toolbar.insert(entry_item, -1)

        vbox = gtk.VBox(False, 1)
        vbox.pack_start(toolbar, False, False, 1)
        toolbar.show_all()

        self.add(vbox)
        vbox.show()
        self.show()

    def entry_activated(self, widget):
        query = widget.get_text().strip()
        if query != "":
            print query

    def on_destroy(self, widget):
        gtk.main_quit()
