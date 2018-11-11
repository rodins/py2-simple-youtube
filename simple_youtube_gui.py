# -*- coding: UTF-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import gobject

import os
import sys

from search_net import SearchNet
from search_task import SearchTask
from image_task import ImageTask
from youtube_dl_processor import VideoIdProcessor
from resolutions_task import ResolutionsTask

EMPTY_POSTER = gtk.gdk.pixbuf_new_from_file(os.path.join(sys.path[0],
                                                         "images",
                                                         "blank_default.png"))
YOUTUBE_PIXBUF = gtk.gdk.pixbuf_new_from_file(os.path.join(sys.path[0],
                                                         "images",
                                                         "youtube_16.png"))

PROG_NAME = "Simple youtube"
COL_PIXBUF = 0
COL_TEXT = 1
ICON_VIEW_ITEM_WIDTH = 150 #350
SPINNER_SIZE = 32
SIDE_WIDTH = 180

class Gui(gtk.Window):
    def __init__(self, API_KEY):
        super(Gui, self).__init__()
        
        self.connect("destroy", self.on_destroy)
        self.set_border_width(5)
        self.set_size_request(780, 400)
        try:
            self.set_icon_from_file(os.path.join(sys.path[0],
                                                 "images", 
                                                 "youtube.png"))
        except Exception, e:
            print e.message

        self.set_title(PROG_NAME)
        self.results_title = ""

        # Toolbar and it's items
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        entry_item = gtk.ToolItem()
        entry = gtk.Entry()
        entry.set_tooltip_text("Search youtube")
        entry.connect("activate", self.entry_activated)
        entry_item.add(entry)
        toolbar.insert(entry_item, -1)

        # Loading indicator
        self.sp_results = gtk.Spinner()
        self.sp_results.set_size_request(SPINNER_SIZE, SPINNER_SIZE)

        # Data
        self.iv_results = gtk.IconView()
        self.iv_results.set_pixbuf_column(COL_PIXBUF)
        self.iv_results.set_text_column(COL_TEXT)
        self.iv_results.set_item_width(ICON_VIEW_ITEM_WIDTH)

        self.results_store = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str)
        self.iv_results.set_model(self.results_store)
        
        self.sw_results = self.create_scrolled_window()
        self.sw_results.add(self.iv_results)
        self.sw_results.show_all()
        vadj = self.sw_results.get_vadjustment()
        vadj.connect("value-changed", self.on_results_scroll_to_bottom)
        self.iv_results.connect("expose-event", self.on_results_draw)
        self.iv_results.connect("item-activated", self.on_result_activated)

        # Error
        btn_results_error = gtk.Button("Repeat")
        btn_results_error.connect("clicked", self.btn_results_error_clicked)
        btn_results_error.show()
        self.hb_results_error = gtk.HBox(False, 1)
        self.hb_results_error.pack_start(btn_results_error, True, False, 10)
        
        self.vb_results = gtk.VBox(False, 1)
        self.vb_results.pack_start(self.sw_results, True, True, 1) 
        self.vb_results.pack_start(self.sp_results, True, False, 1)       
        self.vb_results.pack_start(self.hb_results_error, True, False, 1)

        # Title
        self.lb_title = gtk.Label("")
        self.lb_title.set_size_request(SIDE_WIDTH, -1)
        self.lb_title.set_line_wrap(True)
        fr_title = gtk.Frame("Title")
        fr_title.add(self.lb_title)
        fr_title.show_all()

        # Resolutions
        self.sp_resolutions = gtk.Spinner()
        self.sp_resolutions.set_size_request(SPINNER_SIZE, SPINNER_SIZE)

        self.btn_resolutions_error = gtk.Button("Repeat")
        self.btn_resolutions_error.connect("clicked",
                                           self.btn_resolutions_error_clicked)

        self.tv_resolutions = self.create_tree_view()
        self.resolutions_store = gtk.ListStore(gtk.gdk.Pixbuf, str, str)
        self.tv_resolutions.set_model(self.resolutions_store)
        self.tv_resolutions.connect("row-activated",
                                    self.on_resolution_activated)
        self.tv_resolutions.show()
        
        vb_resolutions = gtk.VBox(False, 1)
        vb_resolutions.pack_start(self.tv_resolutions, True, True, 1)
        vb_resolutions.pack_start(self.sp_resolutions, True, False, 1)
        vb_resolutions.pack_start(self.btn_resolutions_error, True, False, 1)
        vb_resolutions.show()
        
        fr_resolutions = gtk.Frame("Resolutions")
        fr_resolutions.add(vb_resolutions)
        fr_resolutions.show()

        vb_right = gtk.VBox(False, 1)
        vb_right.set_size_request(SIDE_WIDTH, -1)
        vb_right.pack_start(fr_title, False, False, 1)
        vb_right.pack_start(fr_resolutions, True, True, 1)
        vb_right.show()

        hbox = gtk.HBox(False, 1)
        hbox.pack_start(self.vb_results, True, True, 1)
        hbox.pack_start(vb_right, False, False, 1)
        hbox.show()
        
        vbox = gtk.VBox(False, 1)
        vbox.pack_start(toolbar, False, False, 1)
        vbox.pack_start(hbox, True, True, 1)
        toolbar.show_all()
        self.vb_results.show()

        self.add(vbox)
        vbox.show()
        self.show()
        
        self.is_task_started = False
        self.search_net = SearchNet(API_KEY, self)

        self.images_indices = set()
        self.images_cache = {}

        self.video_id_processor = VideoIdProcessor(self)
        self.is_empty = True
        

    def create_scrolled_window(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        return scrolled_window

    def create_tree_view(self):
        tree_view = gtk.TreeView()
        
        renderer_pixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn("Image", renderer_pixbuf, pixbuf=0)
        tree_view.append_column(column)
        
        renderer_text = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Title", renderer_text, text=1)
        tree_view.append_column(column)
        
        tree_view.set_headers_visible(False)
        
        return tree_view

    def start_search_task(self):
        self.is_empty = True
        self.is_task_started = True
        search_task = SearchTask(self.search_net)
        search_task.start()
        
    def entry_activated(self, widget):
        query = widget.get_text().strip()
        if query != "" and not self.is_task_started:
            self.results_title = "Search: " + query
            self.clear_results_model()
            self.search_net.set_query(query)
            self.start_search_task()

    def on_results_scroll_to_bottom(self, adj):
        value = adj.get_value()
        upper = adj.get_upper()
        page_size = adj.get_page_size()
        max_value = value + page_size + page_size
        if max_value > upper and not self.is_task_started and not self.is_empty:
            self.start_search_task()

    def on_results_draw(self, widget, event):
        visible_range = self.iv_results.get_visible_range()
        if visible_range != None:
            index_from = visible_range[0][0]
            index_to = visible_range[1][0] + 1
            
            for index in range(index_from, index_to):
                if index not in self.images_indices:
                    self.images_indices.add(index)
                    # Get image link from model on index
                    row = self.results_store[index]
                    link = row[3] # 3 - image link in model
                    if link != "" and link not in self.images_cache:
                        image_task = ImageTask(link, row, self.images_cache)
                        image_task.start()

    def on_result_activated(self, iconview, path):
        store = iconview.get_model()
        results_iter = store.get_iter(path)
        self.lb_title.set_text(store.get_value(results_iter, 1))
        self.video_id_processor.video_id = store.get_value(results_iter, 2)
        resolutions_task = ResolutionsTask(self.video_id_processor)
        resolutions_task.start()

    def btn_results_error_clicked(self, widget):
        self.start_search_task()

    def on_resolution_activated(self, treeview, path, view_column):
        resolutions_iter = self.resolutions_store.get_iter(path)
        values = self.resolutions_store.get(resolutions_iter, 1, 2)
        self.video_id_processor.play(values[0], values[1])

    def btn_resolutions_error_clicked(self, widget):
        self.video_id_processor.retry()

    def on_destroy(self, widget):
        gtk.main_quit()

    def show_results_loading_indicator(self, is_paging):
        self.set_results_title("Loading...")
        self.sp_results.show()
        self.sp_results.start()
        self.sw_results.set_visible(is_paging)
        self.vb_results.set_child_packing(self.sp_results, 
                                        not is_paging, 
                                        False, 
                                        1, 
                                        gtk.PACK_START)
        self.hb_results_error.hide()

    def show_results_data(self):
        self.set_results_title()
        self.sp_results.hide()
        self.sp_results.stop()
        self.sw_results.show()

    def show_results_error(self, is_paging):
        self.set_results_title("Error")
        self.sp_results.hide()
        self.sp_results.stop()
        self.sw_results.set_visible(is_paging)
        self.vb_results.set_child_packing(self.hb_results_error,
                                         not is_paging,
                                         False,
                                         1,
                                         gtk.PACK_START)
        self.hb_results_error.show()

    def clear_results_model(self):
        self.results_store.clear()
        self.images_indices.clear()

    
    def add_to_results_model(self, title, video_id, image_url):
        self.is_empty = False
        if image_url in self.images_cache:
            self.results_store.append([self.images_cache[image_url],
                                       title,
                                       video_id,
                                       image_url])
        else:
            self.results_store.append([EMPTY_POSTER,
                                       title,
                                       video_id,
                                       image_url])

    def show_resolutions_loading_indicator(self):
        self.resolutions_store.clear()
        self.sp_resolutions.show()
        self.sp_resolutions.start()
        self.tv_resolutions.hide()
        self.btn_resolutions_error.hide()

    def show_resolutions_data(self):
        self.sp_resolutions.hide()
        self.sp_resolutions.stop()
        self.tv_resolutions.show()
        self.btn_resolutions_error.hide()

    def show_resolutions_error(self):
        self.sp_resolutions.hide()
        self.sp_resolutions.stop()
        self.tv_resolutions.hide()
        self.btn_resolutions_error.show()

    def add_to_resolutions_model(self, title, code):
        self.resolutions_store.append([YOUTUBE_PIXBUF, title, code])
            
    def set_task_stopped(self):
        self.is_task_started = False

    def set_results_title(self, title = ""):
        if title == "":
            if self.results_title == "":
                self.set_title(PROG_NAME)
            else:
                self.set_title(PROG_NAME + " - " + self.results_title)
        else:
            self.set_title(PROG_NAME + " - " + title)
