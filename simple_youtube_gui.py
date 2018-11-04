# -*- coding: UTF-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import gobject

COL_PIXBUF = 0
COL_TEXT = 1
ICON_VIEW_ITEM_WIDTH = 180
SPINNER_SIZE = 32

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

        # Loading indicator
        self.sp_results = gtk.Spinner()
        self.sp_results.set_size_request(SPINNER_SIZE, SPINNER_SIZE)

        # Data
        self.iv_results = gtk.IconView()
        self.iv_results.set_pixbuf_column(COL_PIXBUF)
        self.iv_results.set_text_column(COL_TEXT)
        self.iv_results.set_item_width(ICON_VIEW_ITEM_WIDTH)
        self.iv_results.show()
        self.sw_results = self.create_scrolled_window()
        self.sw_results.add(self.iv_results)
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
        self.vb_results.pack_start(self.sp_results, True, False, 1)
        self.vb_results.pack_start(self.sw_results, True, True, 1)        
        self.vb_results.pack_start(self.hb_results_error, True, False, 1)
        
        vbox = gtk.VBox(False, 1)
        vbox.pack_start(toolbar, False, False, 1)
        vbox.pack_start(self.vb_results, True, False, 1)
        toolbar.show_all()
        self.vb_results.show()

        self.add(vbox)
        vbox.show()
        self.show()

    def create_scrolled_window(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        return scrolled_window

    def entry_activated(self, widget):
        query = widget.get_text().strip()
        if query != "":
            print query

    def on_results_scroll_to_bottom(self, adj):
        value = adj.get_value()
        upper = adj.get_upper()
        page_size = adj.get_page_size()
        max_value = value + page_size + page_size
        if max_value > upper:
            print "Scrolled to bottom"

    def on_results_draw(self, widget, event):
        visible_range = self.iv_results.get_visible_range()
        if visible_range != None:
            index_from = visible_range[0][0]
            index_to = visible_range[1][0] + 1
            print index_from
            print index_to
            
##            for index in range(index_from, index_to):
##                if index not in self.range_repeat_set:
##                    self.range_repeat_set.add(index)
##                    # Get image link from model on index
##                    row = self.results_store[index]
##                    link = row[3] # 3 - image link in model
##                    if link != "" and link not in self.images_cache:
##                        image_thread = ImageThread(link, row, self.images_cache)
##                        self.image_threads.append(image_thread)
##                        image_thread.start()

    def on_result_activated(self, iconview, path):
        store = iconview.get_model()
        results_iter = store.get_iter(path)
##        self.saved_item_image = store.get_value(results_iter, 0)
##        self.playlists_title = store.get_value(results_iter, 1)
##        self.actors_link = store.get_value(results_iter, 2)

    def btn_results_error_clicked(self, widget):
        print "On error clicked not implemented"

    def on_destroy(self, widget):
        gtk.main_quit()

    def show_results_loading_indicator(self, is_paging):
        self.sp_results.show()
        self.sp_results.start()
        self.sw_results.set_visible(is_paging)
        self.vb_results.set_child_packing(self.cp_center, 
                                        not is_paging, 
                                        False, 
                                        1, 
                                        gtk.PACK_START)
        self.hb_results_error.hide()

    def show_results_data(self):
        self.sp_results.hide()
        self.sp_results.stop()
        self.sw_results.show()

    def show_results_error(self, is_paging):
        self.sp_results.hide()
        self.sp_results.stop()
        self.sw_results.set_visible(is_paging)
        self.vb_center.set_child_packing(self.hb_center_error,
                                         not is_paging,
                                         False,
                                         1,
                                         gtk.PACK_START)
        self.hb_results_error.show()
