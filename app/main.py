import tkinter as tk
from tkinter import ttk
from app.pages import LoginPage, SignupPage, CalendarPage
from app.pages.menu import MenuBar
from tkcalendar import Calendar
from datetime import date
from app.pages.event_form import EventForm

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.current_user = None

        # -------- Global theme configuration --------
        style = ttk.Style(self)
        print("Available themes:", style.theme_names())
        style.theme_use('clam')

        # Frame/card style
        style.configure("Card.TFrame",
                        background="#f5f5f5",
                        borderwidth=1,
                        relief="raised",
                        padding=20)

        # Headings and labels
        style.configure("Header.TLabel",
                        font=("Bookman Old Style", 18, "bold"),
                        foreground="#333")
        style.configure("TLabel",
                        font=("Arial", 10),
                        background="#f5f5f5")

        # Entries
        style.configure("TEntry",
                        padding=5)

        # Primary buttons (Log in / Sign up)
        style.configure("Primary.TButton",
                        font=("Bookman Old Style", 12),
                        padding=(10,5),
                        background="#4a7a8c",
                        foreground="#fff")
        style.map("Primary.TButton",
                  background=[("active","#6b9aa0"), ("disabled","#ccc")])

        # Link-style button (Sign Up link)
        style.configure("Link.TButton",
                        font=("Arial", 10, "underline"),
                        foreground="#1a5eab",
                        background="#f5f5f5")
        style.map("Link.TButton",
                  foreground=[("active","#003776")])

        # Calendar-specific labels
        style.configure("Calendar.TLabel",
                        font=("Arial", 12),
                        padding=5)
        # --------------------------------------------

        self.title("EventCalendar")
        self.geometry("800x600")

        # Δημιουργία του container frame
        container = ttk.Frame(self, style="Card.TFrame", padding=20)
        container.grid(row=0, column=0, sticky="nsew")
        # κάνε το root window να χωρίζει όλο το χώρο σε 1x1 grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Δημιουργία του calendar widget
        self.calendar = Calendar(container, selectmode='day', year=2023, month=5, day=5)
        self.calendar.grid(row=0, column=0, sticky="nsew", pady=20)

        self.frames = {}
        for PageClass in (LoginPage, SignupPage, CalendarPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.menubar = None
        self.show_frame("LoginPage")
     
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    # Κάλεσε on_show αν υπάρχει
        if hasattr(frame, 'on_show'):
            frame.on_show()
            
    def set_current_user(self, user_obj):
        self.current_user = user_obj            

    def go_to_today(self):
        # Λήψη της τρέχουσας ημερομηνίας
        today = date.today()

        # Ενημέρωση του calendar widget στην τρέχουσα ημερομηνία
        self.calendar.selection_set(today)
        self.calendar.focus_set()    
            
    def open_new_event(self):
        new_event_window = tk.Toplevel(self)
        EventForm(new_event_window)

    def logout(self):
        self.config(menu="")  # αφαιρεί menubar
        self.show_frame("LoginPage")  

    def exit_app(self):
        self.quit()    


    def build_menu(self, **kwargs):
        if self.menubar is not None:
            self.config(menu="")  # remove previous
        self.menubar = MenuBar.build(controller=self, **kwargs)
        self.config(menu=self.menubar)    

if __name__ == "__main__":
    app = Application()
    app.mainloop()