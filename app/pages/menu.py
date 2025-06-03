import tkinter as tk

class MenuBar:
    @staticmethod
    def build(controller, go_to_today, open_year_input, open_all_events, open_new_event, open_delete_event,logout_func, exit_func):
        menu_bar = tk.Menu(controller)
        menu_bar.add_command(label="Σήμερα", command=go_to_today)
        menu_bar.add_command(label="Επιλέξτε έτος", command=open_year_input)
        events_menu = tk.Menu(menu_bar, tearoff=0)
        events_menu.add_command(label="Όλα τα events", command=open_all_events)
        events_menu.add_command(label="Νέο event", command=open_new_event)
        #events_menu.add_command(label="Διαγραφή event", command=open_delete_event)
        menu_bar.add_cascade(label="Events", menu=events_menu)
        logout_menu = tk.Menu(menu_bar,tearoff=0)
        menu_bar.add_cascade(label="Έξοδος",menu=logout_menu)
        logout_menu.add_command(label="Αλλαγή χρήστη",command=logout_func)
        logout_menu.add_command(label="Έξοδος",command=exit_func)

        controller.config(menu=menu_bar)
        return menu_bar
