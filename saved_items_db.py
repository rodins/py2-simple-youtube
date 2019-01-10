# -*- coding: UTF-8 -*-
import os
import sys
import gtk
import sqlite3

#TODO: make calls async
class SavedItemsDb:
    def __init__(self, gui):
        self.gui = gui
        # Extra field in the model is not used but the model must be similar to
        # results model
        self.saved_items_store = gtk.ListStore(gtk.gdk.Pixbuf,
                                               str,
                                               str,
                                               str)
        self.saved_items_position = None

        APP_DIR_NAME = ".simple_youtube"
        SAVES_DIR_NAME = "saves"
        DATA_DIR_NAME = "data"
        DATABASE_NAME = "saved_items.db"
        SAVED_IMAGES_DIR_NAME = "saved_images"

        home_dir = os.path.expanduser("~")
        app_dir = os.path.join(home_dir, APP_DIR_NAME)
        self.app_saves_dir = os.path.join(app_dir, SAVES_DIR_NAME)
        self.app_saved_images_dir = os.path.join(app_dir, SAVED_IMAGES_DIR_NAME)
        
        self.db_directory = os.path.join(app_dir, DATA_DIR_NAME)
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)
        self.db_path = os.path.join(self.db_directory, DATABASE_NAME)
        self.is_table_created = False
        self.copy_from_saves_to_db()

    def open_connection(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()
        
    def set_data(self, pixbuf, title, video_id):
        self.pixbuf = pixbuf
        self.title = title
        self.video_id = video_id
        self.switch_save_delete_buttons()

    def create_table_if_needed(self):
        if not self.is_table_created:
            #TODO: save image to table
            self.cur.execute('CREATE TABLE videos (title TEXT, video_id TEXT)')
            self.is_table_created = True
        
    def list_saved_files(self, button_click = False, on_start = False):
        self.open_connection()
        try:
            saves = self.cur.execute('SELECT * FROM videos').fetchall();
            self.is_table_created = True
            if len(saves) > 0:
                if on_start:
                    self.gui.btn_saved_items.set_active(True)
                self.gui.btn_saved_items.set_sensitive(True)
            else:
                self.disable_btn_saved_items()

            if self.gui.btn_saved_items.get_active(): # Show saved items
                self.results_position = self.gui.get_results_position()
                #TODO: show_results_data. Not updated from results error
                self.gui.btn_prev.set_sensitive(False)
                self.gui.btn_next.set_sensitive(False)
                self.gui.btn_refresh.set_sensitive(False)
                self.gui.set_results_title("Saved items")
                
                self.saved_items_store.clear()
                self.gui.iv_results.set_model(self.saved_items_store)
                for title, video_id in saves:
                    if self.is_image_saved(video_id):
                        self.saved_items_store.append([self.get_image(video_id),
                                                       title,
                                                       video_id,
                                                       None])
                    else:
                        self.saved_items_store.append([self.gui.EMPTY_POSTER,
                                                       title,
                                                       video_id,
                                                       None])
                if self.saved_items_position == None:
                    self.gui.scroll_to_top_of_list(self.saved_items_store)
                else:
                    self.gui.iv_results.scroll_to_path(self.saved_items_position,
                                                       False, 0, 0)
            elif button_click: # Switch back to results
                self.preserve_saved_items_position()
                
                self.gui.results_history.update_prev_next_buttons()
                # FIRST set model
                self.gui.set_results_model()
                # THEN restore position
                if self.results_position != None and self.gui.results_store != None:
                    self.gui.iv_results.scroll_to_path(self.results_position,
                                                       False, 0, 0)
                    self.gui.btn_refresh.set_sensitive(True)
                self.gui.set_results_title()
        except sqlite3.OperationalError as ex:
            print ex
            self.disable_btn_saved_items()
        self.close_connection()

    def btn_save_clicked(self):
        self.save_video_id()
        self.save_image()
        self.switch_save_delete_buttons()
        self.list_saved_files()

    def btn_delete_clicked(self):
        self.remove_video_id()
        self.remove_image()
        self.switch_save_delete_buttons()
        self.list_saved_files()

    def btn_saved_items_clicked(self):
        self.list_saved_files(True)

    def on_search_started(self):
        if self.gui.btn_saved_items.get_active():
            self.gui.btn_saved_items.set_active(False)
            self.list_saved_files(True)

    def disable_btn_saved_items(self):
        self.gui.btn_saved_items.set_sensitive(False)
        self.gui.btn_saved_items.set_active(False)

    def is_video_id_saved(self):
        if not self.is_table_created:
            return False
        self.open_connection()
        cursor = self.cur.execute('SELECT COUNT(video_id) FROM videos WHERE video_id=?',
                         (self.video_id,));
        count = cursor.fetchone()[0]
        is_saved = count > 0
        self.close_connection()
        return is_saved

    def save_video_id(self):
        self.open_connection()
        self.create_table_if_needed()
        self.cur.execute('INSERT INTO videos VALUES (?, ?)',
                        (self.title, self.video_id))
        self.conn.commit()
        self.close_connection()

    def remove_video_id(self):
        self.open_connection()
        self.cur.execute('DELETE FROM videos WHERE video_id=?',
                         (self.video_id,))
        self.conn.commit()
        self.close_connection()

    def is_image_saved(self, video_id):
        path = os.path.join(self.app_saved_images_dir, video_id)
        return os.path.exists(path)

    def get_image(self, video_id):
        path = os.path.join(self.app_saved_images_dir, video_id)
        return gtk.gdk.pixbuf_new_from_file(path)

    def save_image(self):
        if not os.path.exists(self.app_saved_images_dir):
            os.makedirs(self.app_saved_images_dir)
        path = os.path.join(self.app_saved_images_dir, self.video_id)
        if self.pixbuf != None:
                self.pixbuf.save(path, 'png')

    def remove_image(self):
        path = os.path.join(self.app_saved_images_dir, self.video_id)
        if os.path.exists(path):
            os.remove(path)

    def get_saved_title(self, video_id):
        filename = os.path.join(self.app_saves_dir, video_id)
        with open(filename, "r") as f:
            return f.read()

    def remove_file_video_id(self):
        path = os.path.join(self.app_saves_dir, self.video_id)
        if os.path.exists(path):
            os.remove(path)

    def copy_from_saves_to_db(self):
        if os.path.exists(self.app_saves_dir):
            self.open_connection()
            try:
                # Test if table exists
                self.cur.execute('SELECT * FROM videos')
                self.is_table_created = True
            except sqlite3.OperationalError as ex:
                print ex
                self.create_table_if_needed()
            try:
                print "Moving saved files into database..."
                for video_id in os.listdir(self.app_saves_dir):
                    title = self.get_saved_title(video_id)
                    self.cur.execute('INSERT INTO videos VALUES (?, ?)',
                                    (unicode(title), unicode(video_id)))
                    self.video_id = video_id # needed to delete file
                    self.remove_file_video_id()
                self.conn.commit()
                os.rmdir(self.app_saves_dir)
            except OSError as ex:
                print ex
            self.close_connection()

    def switch_save_delete_buttons(self):
        is_saved = self.is_video_id_saved()
        self.gui.btn_save.set_visible(not is_saved)
        self.gui.btn_delete.set_visible(is_saved)
            
    def preserve_saved_items_position(self):
        visible_range = self.gui.iv_results.get_visible_range()
        if visible_range != None:
            self.saved_items_position = visible_range[0][0] # use index_from
        else:
            self.saved_items_position = None      
