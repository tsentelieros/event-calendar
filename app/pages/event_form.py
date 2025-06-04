# app/pages/event_form.py

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from app.controllers import create_event
from app.models import Recurrence, Event


class EventForm:
    def __init__(self, master, owner=None, existing_event=None, on_success=None):
        """
        owner: αντικείμενο User (απαραίτητο για αποθήκευση).
        existing_event: Event προς επεξεργασία (None αν νέο).
        on_success: callback που θα λάβει το αποθηκευμένο Event.
        """
        self.master = master
        self.owner = owner
        self.existing_event = existing_event
        self.on_success = on_success

        self.master.title("Προσθήκη / Επεξεργασία Γεγονότος")
        self.master.geometry("400x650")

        # Διαθέσιμα time slots
        self.time_slots = [f"{h:02d}:00" for h in range(24)]
        self.start_var = tk.StringVar(value=self.time_slots[0])
        self.end_var = tk.StringVar(value=self.time_slots[1])
        self.repeat_var = tk.StringVar(value="Καμία")

        self.build_form()
        self.prefill_if_edit()

    def build_form(self):
        # --- Πεδίο τίτλου ---
        tk.Label(self.master, text="Τίτλος:").pack(anchor="w", padx=10, pady=(10, 0))
        self.title_entry = tk.Entry(self.master, width=50)
        self.title_entry.pack(padx=10, pady=5)

        # --- Περιγραφή ---
        tk.Label(self.master, text="Περιγραφή:").pack(anchor="w", padx=10, pady=(10, 0))
        self.desc_text = tk.Text(self.master, height=4, width=50)
        self.desc_text.pack(padx=10, pady=5)

        # --- Ημερομηνία ---
        tk.Label(self.master, text="Ημερομηνία:").pack(anchor="w", padx=10, pady=(10, 0))
        self.date_entry = DateEntry(self.master, width=30, date_pattern="yyyy-mm-dd")
        self.date_entry.pack(padx=10, pady=5)

        # --- Ώρα Έναρξης ---
        tk.Label(self.master, text="Ώρα Έναρξης:").pack(anchor="w", padx=10, pady=(10, 0))
        tk.OptionMenu(self.master, self.start_var, *self.time_slots).pack(padx=10, pady=5, fill="x")

        # --- Ώρα Λήξης ---
        tk.Label(self.master, text="Ώρα Λήξης:").pack(anchor="w", padx=10, pady=(10, 0))
        self.end_menu = tk.OptionMenu(self.master, self.end_var, *self.time_slots[1:])
        self.end_menu.pack(padx=10, pady=5, fill="x")

        self.start_var.trace_add("write", self.update_end_time_options)

        # --- Χώρος ---
        tk.Label(self.master, text="Χώρος:").pack(anchor="w", padx=10, pady=(10, 0))
        self.location_entry = tk.Entry(self.master, width=50)
        self.location_entry.pack(padx=10, pady=5)

        # --- Επανάληψη ---
        tk.Label(self.master, text="Επανάληψη:").pack(anchor="w", padx=10, pady=(10, 0))
        repeat_opts = ["Καμία", "Ημερήσια", "Εβδομαδιαία", "Μηνιαία", "Ετήσια"]
        tk.OptionMenu(self.master, self.repeat_var, *repeat_opts).pack(padx=10, pady=5, fill="x")
        self.repeat_var.trace_add("write", self.toggle_repeat_until)

        # --- Μέχρι Πότε (εάν ισχύει) ---
        tk.Label(self.master, text="Μέχρι Πότε (αν επαναλαμβάνεται):").pack(anchor="w", padx=10, pady=(10, 0))
        self.repeat_until_entry = DateEntry(
            self.master, width=30, date_pattern="yyyy-mm-dd", state="disabled"
        )
        self.repeat_until_entry.pack(padx=10, pady=5)

        # --- Κουμπί Αποθήκευσης ---
        tk.Button(self.master, text="Αποθήκευση", command=self.save_event).pack(pady=20)

    def prefill_if_edit(self):
        """
        Αν υπάρχει existing_event, προ-γεμίζουμε τα πεδία με τις τωρινές τιμές του.
        """
        ev = self.existing_event
        if not ev:
            return

        # Τίτλος & περιγραφή
        self.title_entry.insert(0, ev.title)
        if ev.description:
            self.desc_text.insert("1.0", ev.description)

        # Ημερομηνία
        self.date_entry.set_date(ev.date)

        # Ώρες
        self.start_var.set(ev.start_time.strftime("%H:%M"))
        self.end_var.set(ev.end_time.strftime("%H:%M"))

        # Χώρος
        if ev.location:
            self.location_entry.insert(0, ev.location)

        # Επανάληψη
        greek_map = {
            Recurrence.NONE:      "Καμία",
            Recurrence.DAILY:     "Ημερήσια",
            Recurrence.WEEKLY:    "Εβδομαδιαία",
            Recurrence.MONTHLY:   "Μηνιαία",
            Recurrence.YEARLY:    "Ετήσια",
        }
        self.repeat_var.set(greek_map.get(ev.recurrence, "Καμία"))
        if ev.recurrence != Recurrence.NONE and ev.recurrence_end:
            self.toggle_repeat_until()
            self.repeat_until_entry.set_date(ev.recurrence_end)

    def update_end_time_options(self, *args):
        selected = self.start_var.get()
        idx = self.time_slots.index(selected)
        allowed = self.time_slots[idx + 1:] or [selected]
        self.end_var.set(allowed[0])

        menu = self.end_menu["menu"]
        menu.delete(0, "end")
        for t in allowed:
            menu.add_command(label=t, command=lambda v=t: self.end_var.set(v))

    def toggle_repeat_until(self, *args):
        state = "normal" if self.repeat_var.get() != "Καμία" else "disabled"
        self.repeat_until_entry.config(state=state)

    def save_event(self):
        # Διαβάζουμε τιμές από τη φόρμα
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end").strip()
        date_ = self.date_entry.get_date()
        start_tm = datetime.strptime(self.start_var.get(), "%H:%M").time()
        end_tm   = datetime.strptime(self.end_var.get(),   "%H:%M").time()
        location = self.location_entry.get().strip()

        # Map επανάληψη σε Recurrence
        rec_map = {
            "Καμία":     Recurrence.NONE,
            "Ημερήσια":  Recurrence.DAILY,
            "Εβδομαδιαία": Recurrence.WEEKLY,
            "Μηνιαία":   Recurrence.MONTHLY,
            "Ετήσια":    Recurrence.YEARLY
        }
        rec = rec_map.get(self.repeat_var.get(), Recurrence.NONE)
        rec_end = None
        if rec != Recurrence.NONE:
            rec_end = self.repeat_until_entry.get_date()

        # Έλεγχος υποχρεωτικών πεδίων
        if not title:
            messagebox.showwarning("Σφάλμα", "Ο τίτλος είναι υποχρεωτικός.")
            return

        # Βεβαιωνόμαστε ότι έχουμε ιδιοκτήτη (owner)
        if self.owner is None:
            messagebox.showerror("Σφάλμα", "Κρίθηκε λάθος: δεν υπάρχει ιδιοκτήτης event.")
            return

        try:
            # Κλήση σε create_event — είτε για νέα εγγραφή, είτε για επεξεργασία
            ev = create_event(
                title=title,
                description=description,
                date_=date_,
                start_time_=start_tm,
                end_time_=end_tm,
                location=location,
                recurrence=rec,
                recurrence_end=rec_end,
                owner=self.owner,
                existing_event=self.existing_event
            )
        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        messagebox.showinfo("Επιτυχία", f"Αποθηκεύτηκε: {ev.title}")

        # Ενημέρωση UI (αν έχουμε callback)
        if self.on_success:
            self.on_success(ev)

        self.master.destroy()
