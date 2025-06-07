import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from app.controllers import create_event
from app.models import Recurrence, Event


class EventForm:
    def __init__(self, master, owner=None, existing_event=None, on_success=None):
        # Αρχικοποίηση παραμέτρων του παραθύρου
        self.master = master
        self.owner = owner  # Χρήστης που δημιουργεί το γεγονός
        self.existing_event = existing_event  # Αν είναι επεξεργασία ήδη υπάρχοντος event
        self.on_success = on_success  # Callback όταν αποθηκευτεί με επιτυχία

        self.master.title("Προσθήκη / Επεξεργασία Γεγονότος")
        self.master.geometry("400x650")

        # Λίστα με διαθέσιμες ώρες (ανά ώρα)
        self.time_slots = [f"{h:02d}:00" for h in range(24)]
        self.start_var = tk.StringVar(value=self.time_slots[0])
        self.end_var = tk.StringVar(value=self.time_slots[1])
        self.repeat_var = tk.StringVar(value="Καμία")

        # Δημιουργία γραφικών στοιχείων
        self.build_form()
        # Αν είναι επεξεργασία, προ-συμπλήρωση των πεδίων
        self.prefill_if_edit()

    def build_form(self):
        # Δημιουργία ετικέτας και πεδίου για τον τίτλο
        tk.Label(self.master, text="Τίτλος:").pack(anchor="w", padx=10, pady=(10, 0))
        self.title_entry = tk.Entry(self.master, width=50)
        self.title_entry.pack(padx=10, pady=5)

        # Πεδίο περιγραφής
        tk.Label(self.master, text="Περιγραφή:").pack(anchor="w", padx=10, pady=(10, 0))
        self.desc_text = tk.Text(self.master, height=4, width=50)
        self.desc_text.pack(padx=10, pady=5)

        # Επιλογή ημερομηνίας γεγονότος
        tk.Label(self.master, text="Ημερομηνία:").pack(anchor="w", padx=10, pady=(10, 0))
        self.date_entry = DateEntry(self.master, width=30, date_pattern="yyyy-mm-dd")
        self.date_entry.pack(padx=10, pady=5)
        # Αν αλλάξει η ημερομηνία, ενημέρωσε και το πεδίο "Μέχρι Πότε"
        self.date_entry.bind("<<DateEntrySelected>>", self.sync_repeat_until_mindate)

        # Επιλογή ώρας έναρξης
        tk.Label(self.master, text="Ώρα Έναρξης:").pack(anchor="w", padx=10, pady=(10, 0))
        tk.OptionMenu(self.master, self.start_var, *self.time_slots).pack(padx=10, pady=5, fill="x")

        # Επιλογή ώρας λήξης (ανάλογα με την έναρξη)
        tk.Label(self.master, text="Ώρα Λήξης:").pack(anchor="w", padx=10, pady=(10, 0))
        self.end_menu = tk.OptionMenu(self.master, self.end_var, *self.time_slots[1:])
        self.end_menu.pack(padx=10, pady=5, fill="x")
        self.start_var.trace_add("write", self.update_end_time_options)

        # Χώρος εκδήλωσης
        tk.Label(self.master, text="Χώρος:").pack(anchor="w", padx=10, pady=(10, 0))
        self.location_entry = tk.Entry(self.master, width=50)
        self.location_entry.pack(padx=10, pady=5)

        # Επιλογή συχνότητας επανάληψης
        tk.Label(self.master, text="Επανάληψη:").pack(anchor="w", padx=10, pady=(10, 0))
        repeat_opts = ["Καμία", "Ημερήσια", "Εβδομαδιαία", "Μηνιαία", "Ετήσια"]
        tk.OptionMenu(self.master, self.repeat_var, *repeat_opts).pack(padx=10, pady=5, fill="x")
        self.repeat_var.trace_add("write", self.toggle_repeat_until)

        # Πεδίο "Μέχρι Πότε" ενεργό μόνο αν υπάρχει επανάληψη
        tk.Label(self.master, text="Μέχρι Πότε (αν επαναλαμβάνεται):").pack(anchor="w", padx=10, pady=(10, 0))
        self.repeat_until_entry = DateEntry(
            self.master, width=30, date_pattern="yyyy-mm-dd", state="disabled"
        )
        self.repeat_until_entry.pack(padx=10, pady=5)

        # Κουμπί αποθήκευσης
        tk.Button(self.master, text="Αποθήκευση", command=self.save_event).pack(pady=20)

    def prefill_if_edit(self):
        # Αν επεξεργαζόμαστε υπάρχον event, προ-συμπληρώνουμε τα πεδία
        ev = self.existing_event
        if not ev:
            return

        self.title_entry.insert(0, ev.title)
        if ev.description:
            self.desc_text.insert("1.0", ev.description)
        self.date_entry.set_date(ev.date)
        self.start_var.set(ev.start_time.strftime("%H:%M"))
        self.end_var.set(ev.end_time.strftime("%H:%M"))
        if ev.location:
            self.location_entry.insert(0, ev.location)

        greek_map = {
            Recurrence.NONE: "Καμία",
            Recurrence.DAILY: "Ημερήσια",
            Recurrence.WEEKLY: "Εβδομαδιαία",
            Recurrence.MONTHLY: "Μηνιαία",
            Recurrence.YEARLY: "Ετήσια",
        }
        self.repeat_var.set(greek_map.get(ev.recurrence, "Καμία"))

        if ev.recurrence != Recurrence.NONE and ev.recurrence_end:
            self.toggle_repeat_until()
            self.repeat_until_entry.set_date(ev.recurrence_end)

        self.sync_repeat_until_mindate()

    def update_end_time_options(self, *args):
        # Ενημέρωση των διαθέσιμων ωρών λήξης ώστε να είναι μετά την ώρα έναρξης
        selected = self.start_var.get()
        idx = self.time_slots.index(selected)
        allowed = self.time_slots[idx + 1:] or [selected]

        self.end_var.set(allowed[0])

        menu = self.end_menu["menu"]
        menu.delete(0, "end")
        for t in allowed:
            menu.add_command(label=t, command=lambda v=t: self.end_var.set(v))

    def toggle_repeat_until(self, *args):
        # Αν ο χρήστης επιλέξει επαναλαμβανόμενο event, ενεργοποιείται το πεδίο "Μέχρι Πότε"
        state = "normal" if self.repeat_var.get() != "Καμία" else "disabled"
        self.repeat_until_entry.config(state=state)

    def sync_repeat_until_mindate(self, event=None):
        # Ορίζει την ελάχιστη ημερομηνία για το πεδίο "Μέχρι Πότε" να είναι η ημερομηνία του γεγονότος
        selected_date = self.date_entry.get_date()
        self.repeat_until_entry.config(mindate=selected_date)
        try:
            if self.repeat_until_entry.get_date() < selected_date:
                self.repeat_until_entry.set_date(selected_date)
        except:
            pass  # Αγνοούμε σφάλματα εάν δεν υπάρχει ημερομηνία ορισμένη ακόμα

    def save_event(self):
        # Ανάγνωση δεδομένων από τη φόρμα
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end").strip()
        date_ = self.date_entry.get_date()
        start_tm = datetime.strptime(self.start_var.get(), "%H:%M").time()
        end_tm = datetime.strptime(self.end_var.get(), "%H:%M").time()
        location = self.location_entry.get().strip()

        rec_map = {
            "Καμία": Recurrence.NONE,
            "Ημερήσια": Recurrence.DAILY,
            "Εβδομαδιαία": Recurrence.WEEKLY,
            "Μηνιαία": Recurrence.MONTHLY,
            "Ετήσια": Recurrence.YEARLY
        }
        rec = rec_map.get(self.repeat_var.get(), Recurrence.NONE)
        rec_end = None
        if rec != Recurrence.NONE:
            rec_end = self.repeat_until_entry.get_date()
            if rec_end < date_:
                messagebox.showerror("Σφάλμα", "Η ημερομηνία επανάληψης δεν μπορεί να είναι πριν την ημερομηνία του γεγονότος.")
                return

        # Έλεγχος υποχρεωτικών πεδίων
        if not title:
            messagebox.showwarning("Σφάλμα", "Ο τίτλος είναι υποχρεωτικός.")
            return

        if self.owner is None:
            messagebox.showerror("Σφάλμα", "Δεν έχει οριστεί ιδιοκτήτης του γεγονότος.")
            return

        # Δημιουργία ή ενημέρωση του γεγονότος
        try:
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

        # Μήνυμα επιτυχίας
        messagebox.showinfo("Επιτυχία", f"Αποθηκεύτηκε: {ev.title}")

        # Εκτέλεση callback αν υπάρχει
        if self.on_success:
            self.on_success(ev)

        # Κλείσιμο παραθύρου
        self.master.destroy()
