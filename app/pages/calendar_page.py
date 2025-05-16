import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import datetime
from app.pages.menu import MenuBar

class CalendarPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_year = datetime.date.today().year
        self.selected_month = datetime.date.today().month

        # Menu bar
        MenuBar.build(
            controller=self.controller,
            go_to_today=self.go_to_today,
            open_year_input=self.open_year_input,
            open_all_events=self.open_all_events,
            open_new_event=self.open_new_event,
            open_delete_event=self.open_delete_event
        )

        # Calendar header frame
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=10, fill='x')
        ttk.Button(header_frame, text='<', style='Calendar.TButton', command=lambda: self.change_month(-1)).pack(side='left')
        self.month_label = ttk.Label(header_frame, text='', style='Calendar.TLabel')
        self.month_label.pack(side='left', expand=True)
        ttk.Button(header_frame, text='>', style='Calendar.TButton', command=lambda: self.change_month(1)).pack(side='right')

        # Days of week header
        days_frame = ttk.Frame(self)
        days_frame.pack()
        self.weekdays = ['Δε', 'Τρ', 'Τε', 'Πε', 'Πα', 'Σα', 'Κυ']
        for idx, day in enumerate(self.weekdays):
            ttk.Label(days_frame, text=day, style='Header.TLabel', anchor='center', width=4).grid(row=0, column=idx, padx=2)

        # Calendar grid
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(pady=5)

        # Schedule frame
        self.schedule_frame = ttk.Frame(self)
        self.schedule_frame.pack(pady=10, fill='both', expand=True)

        # Time display
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        self.time_label = ttk.Label(bottom_frame, font=('Arial', 10))
        self.time_label.pack(side='right')

        self.update_calendar(self.selected_year, self.selected_month)
        self.update_time()

        ttk.Button(self, text="Επιλογή Έτους", command=self.open_year_input).pack()

    def update_calendar(self, year, month):
        self.selected_year = year
        self.selected_month = month
        self.month_label.config(text=f'{calendar.month_name[month]} {year}')

        # Clear old
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Fill calendar days
        days = calendar.monthcalendar(year, month)
        today = datetime.date.today()
        for r, week in enumerate(days, start=1):
            for c, d in enumerate(week):
                text = str(d) if d else ''
                lbl = ttk.Label(self.grid_frame, text=text, style='Calendar.TLabel', anchor='center', width=4)
                lbl.grid(row=r, column=c, padx=2, pady=2)
                if d:
                    # Highlight today
                    if d == today.day and year == today.year and month == today.month:
                        lbl.config(background='#ffebcd', foreground='red')
                    # Hover effect
                    lbl.bind('<Enter>', lambda e, w=lbl: w.state(['!disabled', 'active']))
                    lbl.bind('<Leave>', lambda e, w=lbl: w.state(['!active']))
                    lbl.bind('<Button-1>', lambda e, day=d: self.open_schedule_for_day(day))

    def change_month(self, inc):
        year, month = self.selected_year, self.selected_month + inc
        if month < 1:
            month, year = 12, year-1
        elif month > 12:
            month, year = 1, year+1
        self.update_calendar(year, month)

    def open_year_input(self):
        popup = tk.Toplevel(self.controller)
        popup.title('Επιλογή Έτους')
        popup.resizable(False, False)
        ttk.Label(popup, text='Έτος (1930-2125):').pack(pady=5)
        year_entry = ttk.Entry(popup, justify='center')
        year_entry.pack(pady=5)
        year_entry.focus()
        def set_year(event=None):
            try:
                y = int(year_entry.get())
                if 1930 <= y <= 2125:
                    self.update_calendar(y, self.selected_month)
                    popup.destroy()
                else:
                    messagebox.showerror('Σφάλμα', 'Έτος εκτός ορίων')
            except ValueError:
                messagebox.showerror('Σφάλμα', 'Μη έγκυρος αριθμός')
        year_entry.bind('<Return>', set_year)
        ttk.Button(popup, text='OK', command=set_year).pack(pady=5)

    def go_to_today(self):
        today = datetime.date.today()
        self.update_calendar(today.year, today.month)

    def update_time(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=now)
        self.after(1000, self.update_time)

    def open_schedule_for_day(self, day):
        for w in self.schedule_frame.winfo_children(): w.destroy()
        ttk.Label(self.schedule_frame, text=f'Χρονοδιάγραμμα {day}/{self.selected_month}/{self.selected_year}', font=('Arial', 12, 'bold')).pack(pady=5)
        container = ttk.Frame(self.schedule_frame)
        container.pack(fill='both', expand=True)
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        for hour in range(24):
            row = ttk.Frame(scroll_frame)
            row.pack(fill='x', padx=5, pady=2)
            ttk.Label(row, text=f'{hour:02d}:00', width=8, anchor='w').pack(side='left')
            ttk.Label(row, text='(Καμία καταχώρηση)', foreground='gray').pack(side='left', padx=10)

    # Stubs for MenuBar actions
    def open_all_events(self): messagebox.showinfo('Events','Υπό υλοποίηση')
    def open_new_event (self): messagebox.showinfo('New Event','Υπό υλοποίηση')
    def open_delete_event(self): messagebox.showinfo('Delete Event','Υπό υλοποίηση')

