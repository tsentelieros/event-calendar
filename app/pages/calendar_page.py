import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import datetime

from app.pages.menu import MenuBar
from app.controllers import get_events_on, session
from app.pages.event_form import EventForm
from app.models import Recurrence, Event


class CalendarPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_year = datetime.date.today().year
        self.selected_month = datetime.date.today().month

        self.menu_built = False

        # Header με navigation μήνα
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=10, fill='x')
        ttk.Button(
            header_frame,
            text='<',
            style='Calendar.TButton',
            command=lambda: self.change_month(-1)
        ).pack(side='left')
        self.month_label = ttk.Label(
            header_frame,
            text='',
            style='Calendar.TLabel'
        )
        self.month_label.pack(side='left', expand=True)
        ttk.Button(
            header_frame,
            text='>',
            style='Calendar.TButton',
            command=lambda: self.change_month(1)
        ).pack(side='right')

        # Επικεφαλίδα ημερών
        days_frame = ttk.Frame(self)
        days_frame.pack()
        self.weekdays = ['Δε', 'Τρ', 'Τε', 'Πε', 'Πα', 'Σα', 'Κυ']
        for idx, day in enumerate(self.weekdays):
            ttk.Label(
                days_frame,
                text=day,
                style='Header.TLabel',
                anchor='center',
                width=4
            ).grid(row=0, column=idx, padx=2)

        # Πλέγμα ημερών
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(pady=5)

        # Χρονοδιάγραμμα
        self.schedule_frame = ttk.Frame(self)
        self.schedule_frame.pack(pady=10, fill='both', expand=True)

        # Ώρα κάτω δεξιά
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        self.time_label = ttk.Label(bottom_frame, font=('Arial', 10))
        self.time_label.pack(side='right')

        # Κουμπί επιλογής έτους
        ttk.Button(self, text="Επιλογή Έτους", command=self.open_year_input).pack()

        # Αρχική εμφάνιση
        self.update_calendar(self.selected_year, self.selected_month)
        self.update_time()

    def update_calendar(self, year, month):
        self.selected_year = year
        self.selected_month = month
        self.month_label.config(text=f'{calendar.month_name[month]} {year}')

        # Καθαρισμός προηγούμενων labels
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Γεμίζουμε το πλέγμα με τις ημέρες
        days = calendar.monthcalendar(year, month)
        today = datetime.date.today()
        for r, week in enumerate(days, start=1):
            for c, d in enumerate(week):
                text = str(d) if d else ''
                lbl = ttk.Label(
                    self.grid_frame,
                    text=text,
                    style='Calendar.TLabel',
                    anchor='center',
                    width=4
                )
                lbl.grid(row=r, column=c, padx=2, pady=2)
                if d:
                    # Highlight σημερινής
                    if d == today.day and year == today.year and month == today.month:
                        lbl.config(background='#ffebcd', foreground='red')
                    # Hover effect
                    lbl.bind(
                        '<Enter>',
                        lambda e, w=lbl: (w.state(['!disabled', 'active']), w.config(cursor="hand2"))
                    )
                    lbl.bind(
                        '<Leave>',
                        lambda e, w=lbl: (w.state(['!active']), w.config(cursor="arrow"))
                    )
                    # Click για εμφάνιση χρονοδιαγράμματος
                    lbl.bind('<Button-1>', lambda e, day=d: self.open_schedule_for_day(day))

    def change_month(self, inc):
        year, month = self.selected_year, self.selected_month + inc
        if month < 1:
            month, year = 12, year - 1
        elif month > 12:
            month, year = 1, year + 1
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

    def logout(self):
        self.controller.config(menu="")   # Καθαρίζει το MenuBar
        self.menu_built = False           # Ώστε να ξαναχτιστεί όταν ξαναμπεί χρήστης
        self.controller.show_frame("LoginPage")

    def exit_app(self):
        self.quit()

    def go_to_today(self):
        today = datetime.date.today()
        self.update_calendar(today.year, today.month)

    def update_time(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=now)
        self.after(1000, self.update_time)

    def on_show(self):
        """
        Καλείται κάθε φορά που εμφανίζεται η σελίδα.
        Χτίζει το menu μία φορά.
        """
        if not self.menu_built:
            self.controller.build_menu(
                go_to_today=self.go_to_today,
                open_year_input=self.open_year_input,
                open_all_events=self.open_all_events,
                open_new_event=self.open_new_event,
                open_delete_event=self.open_delete_event,
                logout_func=self.logout,
                exit_func=self.exit_app
            )
            self.menu_built = True

    def open_schedule_for_day(self, day):
        # Καθαρισμός προηγούμενου χρονοδιαγράμματος
        for w in self.schedule_frame.winfo_children():
            w.destroy()

        date_ = datetime.date(self.selected_year, self.selected_month, day)
        ttk.Label(
            self.schedule_frame,
            text=f'Χρονοδιάγραμμα {day}/{self.selected_month}/{self.selected_year}',
            font=('Arial', 12, 'bold')
        ).pack(pady=5)

        events = get_events_on(date_)
        if not events:
            ttk.Label(
                self.schedule_frame,
                text='(Καμία καταχώρηση)',
                foreground='gray'
            ).pack(pady=10)
            return

        # Λίστα events
        for ev in events:
            text = f"{ev.start_time.strftime('%H:%M')} - {ev.end_time.strftime('%H:%M')}  {ev.title}"
            btn = ttk.Button(
                self.schedule_frame,
                text=text,
                command=lambda e=ev: self.edit_event(e)
            )
            btn.pack(fill='x', padx=10, pady=2)

    def open_all_events(self):
        """
        Παράδειγμα: εμφανίζει συνολικό πλήθος όλων των γεγονότων.
        Μπορείς να το επεκτείνεις για πλήρη λίστα.
        """
        all_events = session.query(Event).order_by(Event.date, Event.start_time).all()
        messagebox.showinfo('Events', f'Συνολικά: {len(all_events)} γεγονότα')

    def open_new_event(self):
        """
        Άνοιγμα διαλόγου προσθήκης νέου γεγονότος.
        """
        win = tk.Toplevel(self.controller)

        def refresh(_ev=None):
            self.update_calendar(self.selected_year, self.selected_month)

        EventForm(win, on_success=refresh)

    def open_delete_event(self):
        """
        Μπορείς να υλοποιήσεις διαγραφή εδώ (π.χ. επιλογή από λίστα).
        """
        messagebox.showinfo('Delete Event', 'Υπό υλοποίηση')

    def edit_event(self, ev):
        """
        Άνοιγμα προ-γεμισμένης φόρμας για επεξεργασία υπάρχοντος γεγονότος.
        """
        win = tk.Toplevel(self.controller)

        def refresh(_ev=None):
            self.update_calendar(self.selected_year, self.selected_month)
            self.open_schedule_for_day(ev.date.day)

        form = EventForm(win, on_success=refresh)
        # Προ-γέμισμα πεδίων
        form.title_entry.insert(0, ev.title)
        form.desc_text.insert('1.0', ev.description or '')
        form.date_entry.set_date(ev.date)
        form.start_var.set(ev.start_time.strftime('%H:%M'))
        form.end_var.set(ev.end_time.strftime('%H:%M'))
        form.location_entry.insert(0, ev.location or '')
        greek_map = {
            Recurrence.NONE: "Καμία",
            Recurrence.DAILY: "Ημερήσια",
            Recurrence.WEEKLY: "Εβδομαδιαία",
            Recurrence.MONTHLY: "Μηνιαία",
            Recurrence.YEARLY: "Ετήσια",
        }
        form.repeat_var.set(greek_map.get(ev.recurrence, "Καμία"))
        if ev.recurrence != Recurrence.NONE and ev.recurrence_end:
            form.repeat_until_entry.config(state='normal')
            form.repeat_until_entry.set_date(ev.recurrence_end)
