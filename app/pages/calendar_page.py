# app/pages/calendar_page.py

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

        # ───── Header (πλοήγηση μήνα) ─────
        header_frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        # κάνουμε το header_frame να απλώνεται οριζόντια
        header_frame.columnconfigure(1, weight=1)

        btn_prev = ttk.Button(header_frame, text="<", width=3,
                              command=lambda: self.change_month(-1))
        btn_prev.grid(row=0, column=0, sticky="w")

        self.month_label = ttk.Label(header_frame, text="", anchor="center",
                                     style="Calendar.TLabel")
        self.month_label.grid(row=0, column=1, sticky="ew")

        btn_next = ttk.Button(header_frame, text=">", width=3,
                              command=lambda: self.change_month(1))
        btn_next.grid(row=0, column=2, sticky="e")

        # ───── Πλέγμα ημερολογίου (κεφαλίδες + ημέρες) ─────
        # Βάζουμε όλα σε ένα και μόνο Frame, ώστε οι στήλες να έχουν κοινό grid
        self.grid_frame = ttk.Frame(self, borderwidth=1, relief="flat")
        self.grid_frame.grid(row=1, column=0, sticky="nsew", padx=10)

        # Όταν μεγαλώνει το CalendarPage, το grid_frame να απλώνεται:
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_frame.rowconfigure(0, weight=0)  # κεφαλίδες
        # οι “ημέρες” θα παίρνουν το βάρος κατακόρυφα
        self.grid_frame.rowconfigure(1, weight=1)

        # Γράφουμε τις κεφαλίδες (Δε, Τρ, Τε, …) στην πρώτη γραμμή (row=0)
        self.weekdays = ['Δε', 'Τρ', 'Τε', 'Πε', 'Πα', 'Σα', 'Κυ']
        for col, day in enumerate(self.weekdays):
            lbl = ttk.Label(self.grid_frame, text=day, style="Header.TLabel", anchor="center")
            lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            # κάθε κεφαλίδα να απλώνεται οριζόντια ισότιμα
            self.grid_frame.columnconfigure(col, weight=1)

        # ───── Χρονοδιάγραμμα (κάτω από το ημερολόγιο) ─────
        self.schedule_frame = ttk.Frame(self, relief="flat")
        self.schedule_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        # το schedule_frame δεν παίρνει βάρος σε ύψος, απλώς εμφανίζει τα γεγονότα

        # ───── Ωρολόγιο (κάτω) ─────
        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 5))
        bottom_frame.columnconfigure(0, weight=1)
        self.time_label = ttk.Label(bottom_frame, font=('Arial', 10))
        self.time_label.grid(row=0, column=1, sticky="e")

        # ───── Κουμπί “Επιλογή Έτους” ─────
        btn_year = ttk.Button(self, text="Επιλογή Έτους", command=self.open_year_input)
        btn_year.grid(row=4, column=0, pady=(0, 10))

        # Ορίζουμε ότι όλο το CalendarPage απλώνεται:
        self.rowconfigure(2, weight=0)   # το schedule_frame δεν τεντώνεται κατακόρυφα
        self.rowconfigure(3, weight=0)   # το bottom_frame δεν τεντώνεται
        self.rowconfigure(4, weight=0)   # το κουμπί δεν τεντώνεται

        # ───── Εμφάνιση αρχικά ─────
        self.update_calendar(self.selected_year, self.selected_month)
        self.update_time()

    def update_calendar(self, year, month):
        """
        Γεμίζει (ή ξαναγεμίζει) το πλέγμα με τις ημέρες του δοσμένου (year, month).
        Κάθε αριθμός ημέρας μπαίνει σε grid[row=r, column=c]. Οι αριθμοί ευθυγραμμίζονται
        οριζόντια ακριβώς κάτω από τις αντίστοιχες κεφαλίδες.
        """
        self.selected_year = year
        self.selected_month = month
        self.month_label.config(text=f"{calendar.month_name[month]} {year}")

        # Καθαρίζουμε προηγούμενα “ημερολόγια” (εκτός από τις κεφαλίδες)
        # Οι κεφαλίδες είναι στη row=0· οι ημέρες ξεκινούν από row=1
        for widget in self.grid_frame.grid_slaves():
            info = widget.grid_info()
            if int(info['row']) >= 1:
                widget.destroy()

        # Παίρνουμε τις εβδομάδες του μήνα, π.χ. [[0, 0, 0, 1, 2, 3, 4], …]
        days_matrix = calendar.monthcalendar(year, month)
        today = datetime.date.today()

        for r, week in enumerate(days_matrix, start=1):
            # για κάθε εβδομάδα, r είναι η γραμμή (ξεκινάει από 1)
            self.grid_frame.rowconfigure(r, weight=1)  # ώστε να τεντώνεται κατακόρυφα
            for c, day in enumerate(week):
                text = str(day) if day else ""
                lbl = ttk.Label(
                    self.grid_frame,
                    text=text,
                    style="Calendar.TLabel",
                    anchor="center",
                    relief="flat"
                )
                lbl.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

                if day != 0:
                    # Αν η μέρα είναι η σημερινή, αλλάζουμε χρώμα
                    if (day == today.day and year == today.year and month == today.month):
                        lbl.config(background="#ffebcd", foreground="red")

                    # Hover effect: με αλλαγή κατάστασης state → active
                    lbl.bind("<Enter>", lambda e, w=lbl: (w.state(["active"]), w.config(cursor="hand2")))
                    lbl.bind("<Leave>", lambda e, w=lbl: (w.state(["!active"]), w.config(cursor="arrow")))

                    # Click: άνοιγμα χρονοδιαγράμματος για τη συγκεκριμένη μέρα
                    lbl.bind("<Button-1>", lambda e, d=day: self.open_schedule_for_day(d))

    def change_month(self, inc):
        """
        Προηγούμενος/Επόμενος μήνας
        """
        year, month = self.selected_year, self.selected_month + inc
        if month < 1:
            month, year = 12, year - 1
        elif month > 12:
            month, year = 1, year + 1
        self.update_calendar(year, month)

    def open_year_input(self):
        """
        Ανοίγει popup για επιλογή έτους.
        """
        popup = tk.Toplevel(self.controller)
        popup.title("Επιλογή Έτους")
        popup.resizable(False, False)

        ttk.Label(popup, text="Έτος (1930–2125):").pack(padx=10, pady=(10, 5))
        year_entry = ttk.Entry(popup, justify="center")
        year_entry.pack(padx=10, pady=(0, 10))
        year_entry.focus()

        def set_year(event=None):
            try:
                y = int(year_entry.get())
                if 1930 <= y <= 2125:
                    self.update_calendar(y, self.selected_month)
                    popup.destroy()
                else:
                    messagebox.showerror("Σφάλμα", "Έτος εκτός ορίων.")
            except ValueError:
                messagebox.showerror("Σφάλμα", "Μη έγκυρος αριθμός.")

        year_entry.bind("<Return>", set_year)
        ttk.Button(popup, text="OK", command=set_year).pack(pady=(0, 10))

    def logout(self):
        self.controller.config(menu="")   # Καθαρίζει το MenuBar
        self.menu_built = False
        self.controller.show_frame("LoginPage")

    def exit_app(self):
        self.quit()

    def go_to_today(self):
        """
        Επιστρέφει στο σήμερα
        """
        today = datetime.date.today()
        self.update_calendar(today.year, today.month)

    def update_time(self):
        """
        Εμφανίζει την τρέχουσα ώρα στο κάτω μέρος (κάθε 1 δευτερόλεπτο).
        """
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=now)
        self.after(1000, self.update_time)

    def on_show(self):
        """
        Καλείται κάθε φορά που η σελίδα εμφανίζεται (δηλαδή μετά από login).
        Χτίζει το μενού μόνο την πρώτη φορά.
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
        """
        Εμφανίζει τα γεγονότα για τη συγκεκριμένη μέρα.
        Λαμβάνει υπόψη το current_user.
        """
        # Καθαρίζουμε προηγούμενα γεγονότα
        for w in self.schedule_frame.winfo_children():
            w.destroy()

        date_ = datetime.date(self.selected_year, self.selected_month, day)
        owner = self.controller.current_user

        lbl_title = ttk.Label(
            self.schedule_frame,
            text=f"Χρονοδιάγραμμα {day}/{self.selected_month}/{self.selected_year}",
            font=("Arial", 12, "bold")
        )
        lbl_title.pack(pady=(5, 10))

        if not owner:
            messagebox.showerror("Σφάλμα", "Δεν υπάρχει συνδεδεμένος χρήστης.")
            return

        events = get_events_on(owner, date_)
        if not events:
            ttk.Label(self.schedule_frame,
                      text="(Καμία καταχώρηση)",
                      foreground="gray"
                      ).pack(pady=10)
            return

        # Λέμε σε κάθε γεγονός να εμφανίζεται σε button
        for ev in events:
            text = f"{ev.start_time.strftime('%H:%M')} – {ev.end_time.strftime('%H:%M')}  {ev.title}"
            btn = ttk.Button(
                self.schedule_frame,
                text=text,
                command=lambda e=ev: self.edit_event(e)
            )
            btn.pack(fill="x", padx=10, pady=2)

    def open_all_events(self):
        """
        Εμφανίζει συνολικό αριθμό γεγονότων του τρέχοντα χρήστη.
        """
        owner = self.controller.current_user
        if not owner:
            messagebox.showerror("Σφάλμα", "Δεν υπάρχει συνδεδεμένος χρήστης.")
            return

        all_events = session.query(Event).filter_by(user_id=owner.id) \
            .order_by(Event.date, Event.start_time).all()
        messagebox.showinfo("Events", f"Συνολικά: {len(all_events)} γεγονότα")

    def open_new_event(self):
        """
        Ανοίγει νέο παράθυρο για δημιουργία γεγονότος, περνώντας τον owner στη φόρμα.
        """
        owner = self.controller.current_user
        if not owner:
            messagebox.showerror("Σφάλμα", "Πρέπει να είσαι συνδεδεμένος.")
            return

        win = tk.Toplevel(self.controller)
        def refresher(_ev=None):
            self.update_calendar(self.selected_year, self.selected_month)
        EventForm(win, owner=owner, on_success=refresher)

    def open_delete_event(self):
        """
        Διαγραφή γεγονότος (υπό υλοποίηση).
        """
        messagebox.showinfo("Delete Event", "Υπό υλοποίηση")

    def edit_event(self, ev: Event):
        """
        Άνοιγμα διαλόγου για επεξεργασία υπάρχοντος γεγονότος.
        """
        owner = self.controller.current_user
        if not owner or ev.user_id != owner.id:
            messagebox.showerror("Σφάλμα", "Δεν έχεις δικαίωμα επεξεργασίας.")
            return

        win = tk.Toplevel(self.controller)

        def refresh(updated_ev):
            new_year  = updated_ev.date.year
            new_month = updated_ev.date.month
            new_day   = updated_ev.date.day

            self.update_calendar(new_year, new_month)
            self.open_schedule_for_day(new_day)

        EventForm(win, owner=owner, existing_event=ev, on_success=refresh)
