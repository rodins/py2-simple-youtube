# -*- coding: UTF-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import gobject

import os
import sys
import locale

from search_net import SearchNet
from search_task import SearchTask
from image_task import ImageTask
from youtube_dl_processor import VideoIdProcessor
from resolutions_task import ResolutionsTask
from results_history import ResultsHistory
from saved_items import SavedItems

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
            
            self.EMPTY_POSTER = gtk.gdk.pixbuf_new_from_file(os.path.join(sys.path[0],
                                                             "images",
                                                             "blank_default.png"))
            self.YOUTUBE_PIXBUF = gtk.gdk.pixbuf_new_from_file(os.path.join(sys.path[0],
                                                               "images",
                                                               "youtube_16.png"))
        except Exception, e:
            print e.message

        self.set_title(PROG_NAME)
        self.results_title = ""

        # Toolbar and it's items
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        
        #TODO: change categories image
        btn_categories = gtk.ToggleToolButton(gtk.STOCK_DIRECTORY)
        btn_categories.set_tooltip_text("Show/hide categories")
        btn_categories.connect("clicked", self.btn_categories_clicked)
        toolbar.insert(btn_categories, -1)
        toolbar.insert(gtk.SeparatorToolItem(), -1)

        bookmark_icon = gtk.Image()
        bookmark_icon.set_from_file(os.path.join(sys.path[0], 
                                                "images", 
                                                "bookmark_24.png"))
        
        self.btn_saved_items = gtk.ToggleToolButton()
        self.btn_saved_items.set_icon_widget(bookmark_icon)
        self.btn_saved_items.set_tooltip_text("Show/hide bookmarks")
        self.btn_saved_items.set_sensitive(False)
        self.btn_saved_items.connect("clicked", self.btn_saved_items_clicked)
        toolbar.insert(self.btn_saved_items, -1)
        
        toolbar.insert(gtk.SeparatorToolItem(), -1)

        self.btn_refresh = gtk.ToolButton(gtk.STOCK_REFRESH)
        self.btn_refresh.set_tooltip_text("Update results")
        self.btn_refresh.connect("clicked", self.btn_refresh_clicked)
        self.btn_refresh.set_sensitive(False)
        toolbar.insert(self.btn_refresh, -1)

        toolbar.insert(gtk.SeparatorToolItem(), -1)
        
        self.btn_prev = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.btn_prev.connect("clicked", self.btn_prev_clicked)
        self.btn_prev.set_sensitive(False)
        toolbar.insert(self.btn_prev, -1)
        
        self.btn_next = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.btn_next.connect("clicked", self.btn_next_clicked)
        self.btn_next.set_sensitive(False)
        toolbar.insert(self.btn_next, -1)
        
        toolbar.insert(gtk.SeparatorToolItem(), -1)

        entry_item = gtk.ToolItem()
        entry = gtk.Entry()
        entry.set_tooltip_text("Search youtube")
        entry.connect("activate", self.entry_activated)
        entry_item.add(entry)
        toolbar.insert(entry_item, -1)

        date_icon = gtk.Image()
        date_icon.set_from_file(os.path.join(sys.path[0], 
                                                "images", 
                                                "calendar-24.png"))

        views_icon = gtk.Image()
        views_icon.set_from_file(os.path.join(sys.path[0], 
                                                "images", 
                                                "eye-24.png"))

        self.rtb_date = gtk.RadioToolButton()
        self.rtb_date.set_icon_widget(date_icon)
        self.rtb_date.set_tooltip_text("Sort by date")
        
        self.rtb_views = gtk.RadioToolButton(self.rtb_date)
        self.rtb_views.set_icon_widget(views_icon)
        self.rtb_views.set_tooltip_text("Sort by views")
        
        toolbar.insert(self.rtb_date, -1)
        toolbar.insert(self.rtb_views, -1)

        toolbar.insert(gtk.SeparatorToolItem(), -1)

        self.btn_info = gtk.ToggleToolButton(gtk.STOCK_INFO)
        self.btn_info.set_tooltip_text("Show/hide info")
        self.btn_info.connect("clicked", self.btn_info_clicked)
        toolbar.insert(self.btn_info, -1)

        # Loading indicator
        self.sp_results = gtk.Spinner()
        self.sp_results.set_size_request(SPINNER_SIZE, SPINNER_SIZE)

        # Data
        self.iv_results = gtk.IconView()
        self.iv_results.set_pixbuf_column(COL_PIXBUF)
        self.iv_results.set_text_column(COL_TEXT)
        self.iv_results.set_item_width(ICON_VIEW_ITEM_WIDTH)
        
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

        # No api key label
        lb_api_key = gtk.Label("No youtube api key found. It should be in the file 'key.txt' in the application directory.")
        lb_api_key.set_line_wrap(True)
        
        self.vb_results = gtk.VBox(False, 1)
        self.vb_results.pack_start(self.sw_results, True, True, 1) 
        self.vb_results.pack_start(self.sp_results, True, False, 1)       
        self.vb_results.pack_start(self.hb_results_error, True, False, 1)
        self.vb_results.pack_start(lb_api_key, True, False, 1)

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

        self.sw_resolutions = self.create_scrolled_window()
        self.sw_resolutions.add(self.tv_resolutions)
        self.sw_resolutions.show_all()
        
        vb_resolutions = gtk.VBox(False, 1)
        vb_resolutions.pack_start(self.sw_resolutions, True, True, 1)
        vb_resolutions.pack_start(self.sp_resolutions, True, False, 1)
        vb_resolutions.pack_start(self.btn_resolutions_error, True, False, 1)
        vb_resolutions.show()
        
        fr_resolutions = gtk.Frame("Resolutions")
        fr_resolutions.add(vb_resolutions)
        fr_resolutions.show()

        # Save/delete buttons
        hb_actions = gtk.HBox(False, 1)
        self.btn_save = gtk.Button("Save")
        self.btn_delete = gtk.Button("Delete")
        
        self.btn_save.connect("clicked", self.btn_save_clicked)
        self.btn_delete.connect("clicked", self.btn_delete_clicked)
        
        hb_actions.pack_start(self.btn_save, True, False, 1)
        hb_actions.pack_start(self.btn_delete, True, False, 1)
        hb_actions.show()

        # Client frame
        self.rb_ytdl = gtk.RadioButton(None, "youtube-dl")
        self.rb_streamlink = gtk.RadioButton(self.rb_ytdl, "streamlink")
        vb_client = gtk.VBox(False, 1)
        vb_client.pack_start(self.rb_ytdl, False, False, 1)
        vb_client.pack_start(self.rb_streamlink, False, False, 1)
        self.fr_client = gtk.Frame("Client")
        self.fr_client.add(vb_client)
        self.fr_client.show_all()

        # Player frame
        self.player_init_text = ""
        self.lb_player = gtk.Label("")
        self.lb_player.set_size_request(SIDE_WIDTH, -1)
        self.lb_player.set_line_wrap(True)

        self.btn_close_player = gtk.Button()
        image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_BUTTON)
        self.btn_close_player.set_image(image)
        self.btn_close_player.set_tooltip_text("Close player")
        self.btn_close_player.connect("clicked",
                                      self.btn_close_player_clicked)
        
        hb_player = gtk.HBox(False, 1)
        hb_player.pack_start(self.lb_player, True, True, 1)
        hb_player.pack_end(self.btn_close_player, False, False, 1)
        fr_player = gtk.Frame("Player")
        fr_player.add(hb_player)
        fr_player.show_all()
        self.btn_close_player.hide()

        self.vb_right = gtk.VBox(False, 1)
        self.vb_right.set_size_request(SIDE_WIDTH, -1)
        self.vb_right.pack_start(fr_title, False, False, 1)
        self.vb_right.pack_start(fr_resolutions, True, True, 1)
        self.vb_right.pack_start(hb_actions, False, False, 1)
        self.vb_right.pack_start(self.fr_client, False, False, 1)
        self.vb_right.pack_start(fr_player, False, False, 1)

        # Categories
        self.sp_categories = gtk.Spinner()
        self.sp_categories.set_size_request(SPINNER_SIZE, SPINNER_SIZE)

        self.btn_categories_error = gtk.Button("Repeat")
        self.btn_categories_error.connect("clicked",
                                           self.btn_categories_error_clicked)

        tv_categories = self.create_tree_view()
        self.categories_store = gtk.ListStore(gtk.gdk.Pixbuf, str, str)
        tv_categories.set_model(self.categories_store)
        tv_categories.connect("row-activated", self.on_categories_activated)

        self.sw_categories = self.create_scrolled_window()
        self.sw_categories.add(tv_categories)
        self.sw_categories.show_all()

        self.vb_categories = gtk.VBox(False, 1)
        self.vb_categories.set_size_request(SIDE_WIDTH, -1)
        self.vb_categories.pack_start(self.sp_categories, True, False, 1)
        self.vb_categories.pack_start(self.sw_categories, True, True, 1)
        self.vb_categories.pack_start(self.btn_categories_error, True, False, 1)

        hbox = gtk.HBox(False, 1)
        hbox.pack_start(self.vb_categories, False, False, 1)
        hbox.pack_start(self.vb_results, True, True, 1)
        hbox.pack_start(self.vb_right, False, False, 1)
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
        loc = locale.getlocale()
        self.search_net = SearchNet(API_KEY, self, loc)

        self.images_indices = set()
        self.images_cache = {}

        self.video_id_processor = VideoIdProcessor(self)
        # Setup client radiobuttons if clients detected
        is_ytdl = self.video_id_processor.youtube_dl != ""
        is_streamlink = self.video_id_processor.player.streamlink != ""
        if is_ytdl:
            self.rb_ytdl.set_active(True)
        elif is_streamlink:
            self.rb_streamlink.set_active(True)
        else:
            self.fr_client.hide()

        vb_client.set_sensitive(is_ytdl and is_streamlink)

        self.results_store = None
        self.results_history = ResultsHistory(self)

        self.saved_items = SavedItems(self)
        self.saved_items.list_saved_files(False, True)
        
        self.is_empty = True
        if API_KEY == "":
            lb_api_key.show()
            self.sw_results.hide()
        

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

    def create_new_results_model(self):
        self.results_store = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str)

    def set_results_model(self):
        self.iv_results.set_model(self.results_store)

    def start_search_task(self):
        self.is_empty = True
        self.is_task_started = True
        search_task = SearchTask(self.search_net)
        search_task.start()

    def restore_search_order(self, order):
        self.search_net.order = order
        if order == 'viewCount':
            self.rtb_views.set_active(True)
        elif order == 'date':
            self.rtb_date.set_active(True)

    def is_order_not_matches(self):
        return not (self.rtb_views.get_active() and self.search_net.order == 'viewCount'
                 or self.rtb_date.get_active() and self.search_net.order == 'date')

    def set_search_order(self):
        if self.rtb_views.get_active():
            self.search_net.order = 'viewCount'
        else:
            self.search_net.order = 'date'

    def get_search_data(self, query):
        if self.search_net.query != query or self.is_order_not_matches():
            self.results_history.save_on_new_search()
            self.create_new_results_model()
            self.set_results_model()
            self.results_title = "Search: " + query
            self.search_net.set_query(query)
            self.set_search_order()
        else:
            self.results_store.clear()
        self.images_indices.clear()
        self.search_net.page_token = ""
        self.start_search_task()
        
    def entry_activated(self, widget):
        query = widget.get_text().strip()
        if query != "" and not self.is_task_started:
            self.saved_items.on_search_started()
            self.get_search_data(query)

    def on_results_scroll_to_bottom(self, adj):
        if self.btn_saved_items.get_active():
            return
        value = adj.get_value()
        upper = adj.get_upper()
        page_size = adj.get_page_size()
        max_value = value + page_size + page_size
        if max_value > upper and not self.is_task_started and not self.is_empty:
            self.start_search_task()

    def on_results_draw(self, widget, event):
        if self.btn_saved_items.get_active():
            return
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

    def start_resolutions_task(self):
        if self.fr_client.get_visible():
            resolutions_task = ResolutionsTask(self.video_id_processor)
            resolutions_task.is_ytdl = self.rb_ytdl.get_active()
            resolutions_task.start()
        else:
            self.set_player_text("No youtube-dl or streamlink detected")

    def on_result_activated(self, iconview, path):
        store = iconview.get_model()
        results_iter = store.get_iter(path)
        pixbuf = store.get_value(results_iter, 0)
        title = store.get_value(results_iter, 1)
        video_id = store.get_value(results_iter, 2)
        self.lb_title.set_text(title)
        self.video_id_processor.video_id = video_id
        self.saved_items.set_data(pixbuf, title, video_id)
        self.start_resolutions_task()

    def btn_results_error_clicked(self, widget):
        self.start_search_task()

    def on_resolution_activated(self, treeview, path, view_column):
        resolutions_iter = self.resolutions_store.get_iter(path)
        values = self.resolutions_store.get(resolutions_iter, 1, 2)
        self.video_id_processor.play(values[0], values[1])

    def btn_resolutions_error_clicked(self, widget):
        self.start_resolutions_task()

    def on_destroy(self, widget):
        gtk.main_quit()

    def show_results_loading_indicator(self, is_paging):
        self.set_results_title("Loading...")
        self.btn_refresh.set_sensitive(False)
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
        self.btn_refresh.set_sensitive(True)
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
            self.results_store.append([self.EMPTY_POSTER,
                                       title,
                                       video_id,
                                       image_url])

    def show_resolutions_loading_indicator(self):
        self.resolutions_store.clear()
        self.btn_close_player.hide()
        self.vb_right.show()
        self.btn_info.set_active(True)
        self.set_player_init_text()
        self.sp_resolutions.show()
        self.sp_resolutions.start()
        self.sw_resolutions.hide()
        self.btn_resolutions_error.hide()

    def show_resolutions_data(self):
        self.sp_resolutions.hide()
        self.sp_resolutions.stop()
        self.sw_resolutions.show()
        self.btn_resolutions_error.hide()

    def show_resolutions_error(self):
        self.sp_resolutions.hide()
        self.sp_resolutions.stop()
        self.sw_resolutions.hide()
        self.btn_resolutions_error.show()

    def add_to_resolutions_model(self, title, code):
        self.resolutions_store.append([self.YOUTUBE_PIXBUF, title, code])

    def set_player_init_text(self, text=""):
        if text != "":
            self.init_player_text = text
        self.set_player_text(self.init_player_text)

    def set_player_text(self, text):
        self.lb_player.set_text(text)

    def btn_close_player_clicked(self, widget):
        self.video_id_processor.player.kill()

    def show_close_player_button(self):
        self.btn_close_player.show()

    def btn_info_clicked(self, widget):
        self.vb_right.set_visible(widget.get_active())

    def btn_refresh_clicked(self, widget):
        self.get_search_data(self.search_net.query)

    def btn_prev_clicked(self, widget):
        self.results_history.btn_prev_clicked()

    def btn_next_clicked(self, widget):
        self.results_history.btn_next_clicked()

    def btn_saved_items_clicked(self, widget):
        self.saved_items.btn_saved_items_clicked()

    def btn_save_clicked(self, widget):
        self.saved_items.btn_save_clicked()

    def btn_delete_clicked(self, widget):
        self.saved_items.btn_delete_clicked()

    def btn_categories_clicked(self, widget):
        self.vb_categories.set_visible(widget.get_active())
        if widget.get_active():
            self.show_categories_loading_indicator()
        else:
            self.show_categories_data()
            

    def btn_categories_error_clicked(self, widget):
        print "Categories error clicked"

    def on_categories_activated(self, treeview, path, view_column):
        print "On categories activated"

    def show_categories_loading_indicator(self):
        self.sp_categories.show()
        self.sp_categories.start()
        self.sw_categories.hide()
        self.btn_categories_error.hide()

    def show_categories_data(self):
        self.sp_categories.hide()
        self.sp_categories.stop()
        self.sw_categories.show()

    def show_categories_error(self):
        self.sp_categories.hide()
        self.sp_categories.stop()
        self.btn_categories_error.show()

    def get_results_position(self):
        visible_range = self.iv_results.get_visible_range()
        if visible_range != None:
            return visible_range[1][0] # use index_to as position
        return None

    def set_results_position(self, position):
        if position != None:
            self.iv_results.scroll_to_path(position, False, 0, 0)

    def scroll_to_top_of_list(self, store):
        if store != None:
            first_iter = store.get_iter_first()
            first_path = store.get_path(first_iter)
            self.iv_results.scroll_to_path(first_path, False, 0, 0)
            
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
