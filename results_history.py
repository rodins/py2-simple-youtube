# -*- coding: UTF-8 -*-

class SavedResults:
    def __init__(self):
        self.title = ""
        self.store = ""
        self.query = ""
        self.page_token = ""
        self.position = ""
        self.order = ""

class ResultsHistory:
    def __init__(self, gui):
        self.gui = gui
        self.back_stack = []
        self.forward_stack = []

    def get_current_results(self):
        saved_results = SavedResults()
        saved_results.title = self.gui.results_title
        saved_results.store = self.gui.results_store
        saved_results.query = self.gui.search_net.query
        saved_results.page_token = self.gui.search_net.page_token
        saved_results.position = self.gui.get_results_position()
        saved_results.order = self.gui.search_net.order
        return saved_results

    def restore_from_saved_results(self, saved_results):
        self.gui.results_title = saved_results.title
        self.gui.set_results_title()
        self.gui.results_store = saved_results.store
        self.gui.images_indices.clear()
        self.gui.set_results_model()
        self.gui.show_results_data()
        self.gui.search_net.query = saved_results.query
        self.gui.search_net.page_token = saved_results.page_token
        self.gui.set_results_position(saved_results.position)
        self.gui.restore_search_order(saved_results.order)

    def update_prev_next_buttons(self):
        prev_size = len(self.back_stack)
        next_size = len(self.forward_stack)
        # Set top item titles as tooltips for buttons
        if(prev_size > 0):
            top_item = self.back_stack[prev_size-1]
            self.gui.btn_prev.set_tooltip_text(top_item.title)
        else:
            self.gui.btn_prev.set_tooltip_text("No previous history")

        if(next_size > 0):
            top_item = self.forward_stack[next_size-1]
            self.gui.btn_next.set_tooltip_text(top_item.title)
        else:
            self.gui.btn_next.set_tooltip_text("No next history")

        # Emable buttons if lists are not empty, disable otherwise    
        self.gui.btn_prev.set_sensitive(prev_size > 0)
        self.gui.btn_next.set_sensitive(next_size > 0)

    def save_on_new_search(self):
        if self.gui.results_store != None:
            self.back_stack.append(self.get_current_results())
            self.forward_stack = []
            self.update_prev_next_buttons()
    
    def btn_prev_clicked(self):
        self.forward_stack.append(self.get_current_results())
        self.restore_from_saved_results(self.back_stack.pop())
        self.update_prev_next_buttons()

    def btn_next_clicked(self):
        self.back_stack.append(self.get_current_results())
        self.restore_from_saved_results(self.forward_stack.pop())
        self.update_prev_next_buttons()
        
