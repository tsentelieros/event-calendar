import tkinter as tk
from tkinter import ttk
from app.pages import LoginPage, SignupPage, CalendarPage
from app.pages.menu import MenuBar

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
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


        container = ttk.Frame(self, style="Card.TFrame", padding=20)
        container.grid(row=0, column=0, sticky="nsew")
        # κάνε το root window να χωρίζει όλο το χώρο σε 1x1 grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for PageClass in (LoginPage, SignupPage, CalendarPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        MenuBar.build(
            controller=self,
            go_to_today=lambda: None,
            open_year_input=lambda: None,
            open_all_events=lambda: None,
            open_new_event=lambda: None,
            open_delete_event=lambda: None
        )

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
